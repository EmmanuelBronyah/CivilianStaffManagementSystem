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
from rest_framework.response import Response
from rest_framework import status
from .services import (
    cache_temp_token,
    send_otp_email_task,
    get_temp_token,
    delete_temp_token,
)
from django.db import transaction


logger = logging.getLogger(__name__)


# * USER
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.RetrieveCreateUserSerializer
    queryset = CustomUser.objects.all()
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.UserReadSerializer(self.user)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        with transaction.atomic():
            self.user = serializer.save(
                created_by=self.request.user, updated_by=self.request.user
            )
            logger.debug(f"User Account({self.user}) created.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} added a new User(Username: {self.user.username})",
            )
            logger.debug(
                f"Activity feed({self.request.user} added a new User(Username: {self.user.username})) created."
            )


class RetrieveUserView(generics.RetrieveAPIView):
    serializer_class = serializers.UserReadSerializer
    queryset = CustomUser.objects.select_related(
        "created_by", "updated_by", "grade", "division"
    )
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]


class RetrieveAllUsersView(generics.ListAPIView):
    serializer_class = serializers.UserReadSerializer
    queryset = CustomUser.objects.select_related(
        "created_by", "updated_by", "grade", "division"
    )
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = serializers.RetrieveUpdateDestroyUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.UserReadSerializer(self.user)

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        with transaction.atomic():
            self.user = serializer.save(updated_by=self.request.user)
            logger.debug(f"User Account({self.user}) updated.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated User Account(Username: {self.user.username})",
            )
            logger.debug(
                f"Activity feed({self.request.user} updated User Account(Username: {self.user.username})) created."
            )


class DeactivateUserView(generics.DestroyAPIView):
    serializer_class = serializers.RetrieveUpdateDestroyUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            instance.is_active = False
            instance.save()
            logger.debug(f"User Account({instance}) deactivated.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"User Account(Username: {instance.username}) was deactivated by {self.request.user}",
            )
            logger.debug(
                f"Activity feed(User Account(Username: {instance.username}) was deactivated by {self.request.user}) created."
            )

        return Response(
            {"detail": "User Account deactivated."}, status=status.HTTP_200_OK
        )


class RestoreUserAccountView(generics.UpdateAPIView):
    serializer_class = serializers.RetrieveUpdateDestroyUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            instance.is_active = True
            instance.save()
            logger.debug(f"User Account({instance}) restored.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"User Account(Username: {instance.username}) was restored by {self.request.user}",
            )
            logger.debug(
                f"Activity feed(User Account(Username: {instance.username}) was restored by {self.request.user}) created."
            )

        return Response({"detail": "User Account restored."}, status=status.HTTP_200_OK)


class DeleteUserView(generics.DestroyAPIView):
    serializer_class = serializers.RetrieveUpdateDestroyUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_destroy(self, instance):
        with transaction.atomic():
            username = instance.username
            instance.delete()
            logger.debug(f"User Account(Username: {instance}) deleted.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"User Account(Username: {username}) was deleted by {self.request.user}",
            )
            logger.debug(
                f"Activity feed(User Account(Username: {username}) was deleted by {self.request.user}) created."
            )


# * DIVISION
class CreateDivisionAPIView(generics.CreateAPIView):
    queryset = models.Divisions.objects.all()
    serializer_class = serializers.DivisionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        with transaction.atomic():
            division = serializer.save()
            logger.debug(f"Division({division}) created.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} added a new Division({division.division_name})",
            )
            logger.debug(
                f"Activity feed({self.request.user} added a new Division({division.division_name})) created."
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
        with transaction.atomic():
            previous_division = self.get_object()
            previous_division_name = previous_division.division_name

            division = serializer.save()
            logger.debug(f"Division({previous_division_name}) updated.")

            changes = previous_division_name != division.division_name

            if changes:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=f"{self.request.user} updated Division({previous_division_name}): {previous_division_name} → {division.division_name}",
                )
                logger.debug(
                    f"Activity feed({self.request.user} updated Division({previous_division_name}): {previous_division_name} → {division.division_name}) created."
                )


class DeleteDivisionAPIView(generics.DestroyAPIView):
    queryset = models.Divisions.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.DivisionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        with transaction.atomic():
            division_name = instance.division_name
            instance.delete()
            logger.debug(f"Division({division_name}) deleted.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"Division({division_name}) was deleted by {self.request.user}",
            )
            logger.debug(
                f"Activity feed(Division({division_name}) was deleted by {self.request.user}') deleted."
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

        if not user:
            logger.warning("User credentials provided is invalid.")

            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_cache_key = f"otp_email_sent:{user.id}"
        if cache.get(otp_cache_key):

            logger.debug(f"OTP already sent.")

            return Response({"detail": "OTP already sent."}, status=status.HTTP_200_OK)

        temp_token = f"otp_token:{uuid.uuid4()}"

        logger.debug(f"Temporary token has been created for user({user}).")

        device = None

        try:
            cache_temp_token(temp_token, user.id)

            logger.info(f"OTP will be dully sent to user's({user}'s) email.")

            device, _ = EmailDevice.objects.get_or_create(user=user, name="default")
            send_otp_email_task.delay(device.id)

            cache.set(otp_cache_key, True, timeout=60)

        except Exception as e:
            logger.exception(f"Temporary server error: {e}")

            if device:
                device.delete()

            return Response(
                {"detail": "Temporary server issue. Please try again shortly."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {"detail": "OTP sent to your email.", "temp_token": temp_token},
            status=status.HTTP_200_OK,
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

        if not all([temp_token, otp_token]):
            delete_temp_token(temp_token)
            logger.warning("Invalid OTP. Please start the login process again.")

            return Response(
                {"detail": "Invalid OTP. Please start the login process again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = get_temp_token(temp_token)

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

            delete_temp_token(temp_token)
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


class ResendOTPView(APIView):
    http_method_names = ["post"]
    throttle_classes = [CustomAnonRateThrottle, CustomUserRateThrottle]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = serializers.VerifyOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tokens = serializer.validated_data.get("tokens", None)
        temp_token = tokens.get("temp_token", None)
        user_id = get_temp_token(temp_token)

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

        logger.info(f"OTP will be dully sent to user's({user}'s) email.")

        device, _ = EmailDevice.objects.get_or_create(user=user, name="default")
        send_otp_email_task.delay(device.id)

        return Response(
            {"detail": "OTP sent to your email.", "temp_token": temp_token},
            status=status.HTTP_200_OK,
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
