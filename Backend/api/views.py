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
from .throttles import CustomAnonRateThrottle, CustomUserRateThrottle, UserRateThrottle
import logging
from . import models
from activity_feeds.models import ActivityFeeds
from django.utils import timezone

logger = logging.getLogger(__name__)


# * USER
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.RetrieveCreateUserSerializer
    queryset = CustomUser.objects.all()
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        user = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new user: {user.username}",
        )


class RetrieveUserView(generics.RetrieveAPIView):
    serializer_class = serializers.RetrieveUpdateDestroyUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "pk"
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated]


class RetrieveAllUsersView(generics.ListAPIView):
    serializer_class = serializers.RetrieveCreateUserSerializer
    queryset = CustomUser.objects.all()
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated]


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = serializers.RetrieveUpdateDestroyUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "pk"
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        user = serializer.save(updated_by=self.request.user)

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated account details for: {user.username}",
        )


class DeactivateUserView(generics.DestroyAPIView):
    serializer_class = serializers.RetrieveUpdateDestroyUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "pk"
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"User account '{instance.username}' was deactivated by {self.request.user}",
        )

        return Response(
            {"detail": "User account deactivated."}, status=status.HTTP_200_OK
        )


class RestoreUserAccountView(generics.UpdateAPIView):
    serializer_class = serializers.RetrieveUpdateDestroyUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "pk"
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"User account '{instance.username}' was restored by {self.request.user}",
        )

        return Response({"detail": "User account restored."}, status=status.HTTP_200_OK)


class DeleteUserView(generics.DestroyAPIView):
    serializer_class = serializers.RetrieveUpdateDestroyUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "pk"
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_destroy(self, instance):
        username = instance.username
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"User account {username} was deleted by {self.request.user}",
        )


# * DIVISION
class CreateDivisionAPIView(generics.CreateAPIView):
    queryset = models.Divisions.objects.all()
    serializer_class = serializers.DivisionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        division = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new division: {division.division_name}",
        )


class RetrieveDivisionAPIView(generics.RetrieveAPIView):
    queryset = models.Divisions.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.DivisionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListDivisionsAPIView(generics.ListAPIView):
    queryset = models.Divisions.objects.all()
    serializer_class = serializers.DivisionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EditDivisionAPIView(generics.UpdateAPIView):
    queryset = models.Divisions.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.DivisionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_division = self.get_object()
        previous_division_name = previous_division.division_name

        division = serializer.save()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} modified division from '{previous_division_name}' to '{division.division_name}'",
        )


class DeleteDivisionAPIView(generics.DestroyAPIView):
    queryset = models.Divisions.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.DivisionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        division_name = instance.division_name
        instance.delete()

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"Division '{division_name}' was deleted by {self.request.user}",
        )


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
