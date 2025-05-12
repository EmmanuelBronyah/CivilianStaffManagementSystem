from rest_framework.views import APIView
from rest_framework import generics
from .serializers import ListCreateUserSerializer, LoginSerializer, VerifyOTPSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django_otp.plugins.otp_email.models import EmailDevice
from django.core.cache import cache
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.views.generic.base import RedirectView
from django.conf import settings
from . import network_exceptions
from .throttles import CustomAnonRateThrottle, CustomUserRateThrottle


class ListUsersView(generics.ListAPIView):
    serializer_class = ListCreateUserSerializer
    queryset = CustomUser.objects.all()
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated]


class CreateUserView(generics.CreateAPIView):
    serializer_class = ListCreateUserSerializer
    queryset = CustomUser.objects.all()
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [AllowAny]


class LoginView(APIView):
    http_method_names = ["post"]
    throttle_classes = [CustomAnonRateThrottle, CustomUserRateThrottle]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username", None)
        password = serializer.validated_data.get("password", None)
        user = authenticate(request, username=username, password=password)

        try:

            if not user:
                return Response(
                    {"Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST
                )

            device, _ = EmailDevice.objects.get_or_create(user=user, name="default")
            device.generate_challenge()

            str_uuid = str(uuid.uuid4())
            temp_token = f"otp_token:{str_uuid}"
            cache.set(temp_token, user.id, timeout=300)

            return Response(
                {"detail": "OTP sent to your email.", "temp_token": temp_token},
                status=status.HTTP_200_OK,
            )

        except network_exceptions.REDIS_ERRORS as e:
            device.delete()
            return Response(
                {"error": "Temporary server issue. Please try again shortly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except network_exceptions.NETWORK_EXCEPTIONS as e:
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
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data.get("tokens", None)
        temp_token = tokens.get("temp_token", None)
        otp_token = tokens.get("otp_token", None)

        try:

            if not all([temp_token, otp_token]):
                cache.delete(temp_token)
                return Response(
                    {"detail": "Invalid OTP. Please start the login process again."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_id = cache.get(temp_token)

            if user_id is None:
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

                return Response(
                    {
                        "refresh_token": str(refresh),
                        "access_token": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "detail": "Token expired or invalid. Please start the login process again."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except network_exceptions.REDIS_ERRORS as e:
            return Response(
                {"error": "Temporary server issue. Please try again shortly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except network_exceptions.NETWORK_EXCEPTIONS as e:
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
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data.get("tokens", None)
        temp_token = tokens.get("temp_token", None)
        user_id = cache.get(temp_token)

        try:

            if user_id is None:
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

            return Response(
                {"detail": "OTP sent to your email.", "temp_token": temp_token},
                status=status.HTTP_200_OK,
            )

        except network_exceptions.REDIS_ERRORS as e:
            device.delete()
            return Response(
                {"error": "Temporary server issue. Please try again shortly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except network_exceptions.NETWORK_EXCEPTIONS as e:
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

            return (
                f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
            )

        except network_exceptions.NETWORK_EXCEPTIONS as e:
            return Response(
                {
                    "detail": "Network issue detected. Please ensure you are connected to the internet and try again."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
