from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from .serializers import ListCreateUserSerializer, LoginSerializer, VerifyOTPSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django_otp.plugins.otp_email.models import EmailDevice
from django.core.cache import cache
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny


class ListCreateUserView(ListCreateAPIView):
    serializer_class = ListCreateUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]


class LoginView(APIView):
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username", None)
        password = serializer.validated_data.get("password", None)
        user = authenticate(request, username=username, password=password)

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


class VerifyOTPView(APIView):
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data.get("tokens", None)
        temp_token = tokens.get("temp_token", None)
        otp_token = tokens.get("otp_token", None)

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
                    "temp_token": temp_token,
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


class ResendOTPView(APIView):
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data.get("tokens", None)
        temp_token = tokens.get("temp_token", None)
        user_id = cache.get(temp_token)

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
