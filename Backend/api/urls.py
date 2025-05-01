from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register/", views.ListCreateUserView.as_view(), name="register-user"),
    path("login/", views.LoginView.as_view(), name="user-login"),
    path("verify-otp-token/", views.VerifyOTPView.as_view(), name="token-verification"),
    path("resend-otp/", views.ResendOTPView.as_view(), name="otp-resend"),
    path("token-refresh/", TokenRefreshView.as_view(), name="refresh-tokens"),
    path("users/", views.ListCreateAPIView.as_view(), name="lists-users"),
]
