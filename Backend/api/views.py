from rest_framework.views import APIView
from rest_framework import generics
from . import serializers
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django_otp.plugins.otp_email.models import EmailDevice
from django.core.cache import cache
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.views.generic.base import RedirectView
from django.conf import settings
from . import network_exceptions
from .throttles import CustomAnonRateThrottle, CustomUserRateThrottle
import logging

logger = logging.getLogger(__name__)


class ListUsersView(generics.ListAPIView):
    serializer_class = serializers.ListCreateUserSerializer
    queryset = CustomUser.objects.all()
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated]


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.ListCreateUserSerializer
    queryset = CustomUser.objects.all()
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [AllowAny]


class LoginView(APIView):
    http_method_names = ["post"]
    throttle_classes = [CustomAnonRateThrottle, CustomUserRateThrottle]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username", None)
        password = serializer.validated_data.get("password", None)
        user = authenticate(request, username=username, password=password)
        logger.debug(f"User found: {user}")
        try:

            if not user:
                logger.warning("User credentials provided is invalid.")
                return Response(
                    {"detail": "Invalid credentials."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            device, _ = EmailDevice.objects.get_or_create(user=user, name="default")
            device.generate_challenge()
            str_uuid = str(uuid.uuid4())
            temp_token = f"otp_token:{str_uuid}"
            logger.debug(f"Temporary token has been created for user({user})")
            cache.set(temp_token, user.id, timeout=300)

            logger.info(f"OTP will be dully sent to user's({user}'s) email.")
            return Response(
                {"detail": "OTP sent to your email.", "temp_token": temp_token},
                status=status.HTTP_200_OK,
            )

        except network_exceptions.REDIS_ERRORS as e:
            logger.exception(f"A redis server error occurred. Exception({e})")
            device.delete()
            return Response(
                {"detail": "Temporary server issue. Please try again shortly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except network_exceptions.NETWORK_EXCEPTIONS as e:
            logger.exception(f"A network error occurred. Exception({e})")
            device.delete()
            return Response(
                {
                    "detail": "Network issue detected. Please ensure you are connected to the internet and try again."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class VerifyOTPView(APIView):
    http_method_names = ["post"]
    throttle_classes = [CustomAnonRateThrottle, CustomUserRateThrottle]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = serializers.VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data.get("tokens", None)
        temp_token = tokens.get("temp_token", None)
        otp_token = tokens.get("otp_token", None)

        try:

            if not all([temp_token, otp_token]):
                cache.delete(temp_token)
                logger.warning("Invalid OTP. Please start the login process again.")
                return Response(
                    {"detail": "Invalid OTP. Please start the login process again."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_id = cache.get(temp_token)

            if user_id is None:
                logger.warning(
                    "Token expired or invalid. Please start the login process again."
                )
                return Response(
                    {
                        "detail": "Token expired or invalid. Please start the login process again.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = CustomUser.objects.get(id=user_id)
            device = EmailDevice.objects.filter(user=user, name="default").first()

            if device and device.verify_token(otp_token):
                refresh = RefreshToken.for_user(user)
                cache.delete(temp_token)
                logger.info(
                    "User has been verified. Refresh and access token will be dully created."
                )
                return Response(
                    {
                        "refresh_token": str(refresh),
                        "access_token": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )

            logger.warning(
                "Token expired or invalid. Please start the login process again."
            )
            return Response(
                {
                    "detail": "Token expired or invalid. Please start the login process again."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except network_exceptions.REDIS_ERRORS as e:
            logger.exception(f"A redis server error occurred. Exception({e})")
            return Response(
                {"detail": "Temporary server issue. Please try again shortly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except network_exceptions.NETWORK_EXCEPTIONS as e:
            logger.exception(f"A network error occurred. Exception({e})")
            return Response(
                {
                    "detail": "Network issue detected. Please ensure you are connected to the internet and try again."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class ResendOTPView(APIView):
    http_method_names = ["post"]
    throttle_classes = [CustomAnonRateThrottle, CustomUserRateThrottle]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = serializers.VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data.get("tokens", None)
        temp_token = tokens.get("temp_token", None)
        user_id = cache.get(temp_token)

        try:

            if user_id is None:
                logger.warning(
                    "Your session has expired. Please start the login process again."
                )
                return Response(
                    {
                        "detail": "Your session has expired. Please start the login process again."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = CustomUser.objects.get(id=user_id)
            device = EmailDevice.objects.filter(user=user, name="default").first()

            if device:
                device.delete()

            device, _ = EmailDevice.objects.get_or_create(user=user, name="default")
            device.generate_challenge()

            logger.info(f"OTP will be dully sent to user's({user}'s) email.")
            return Response(
                {"detail": "OTP sent to your email.", "temp_token": temp_token},
                status=status.HTTP_200_OK,
            )

        except network_exceptions.REDIS_ERRORS as e:
            logger.exception(f"A redis server error occurred. Exception({e})")
            device.delete()
            return Response(
                {"detail": "Temporary server issue. Please try again shortly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except network_exceptions.NETWORK_EXCEPTIONS as e:
            logger.exception(f"A network error occurred. Exception({e})")
            device.delete()
            return Response(
                {
                    "detail": "Network issue detected. Please ensure you are connected to the internet and try again."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class PasswordResetConfirmRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        try:

            uidb64 = kwargs.get("uidb64")
            token = kwargs.get("token")

            logger.debug("Password reset url will be dully sent to user's email.")
            return (
                f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
            )

        except network_exceptions.NETWORK_EXCEPTIONS as e:
            logger.exception(f"A network error occurred. Exception({e})")
            return Response(
                {
                    "detail": "Network issue detected. Please ensure you are connected to the internet and try again."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class LogoutView(APIView):
    http_method_names = ["post"]
    throttle_classes = [CustomAnonRateThrottle, CustomUserRateThrottle]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data.get("refresh_token", None)

        try:

            token = RefreshToken(refresh_token)
            token.blacklist()

            logger.info("You have been successfully logged out.")
            return Response(
                {"detail": "You have been successfully logged out."},
                status=status.HTTP_204_NO_CONTENT,
            )

        except TokenError as e:
            logger.warning("Invalid or expired token.")
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except network_exceptions.NETWORK_EXCEPTIONS as e:
            logger.exception(f"A network error occurred. Exception({e})")
            return Response(
                {
                    "detail": "Network issue detected. Please ensure you are connected to the internet and try again."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
