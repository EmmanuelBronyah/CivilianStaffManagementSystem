from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView


urlpatterns = [
    # Register
    path("register/", views.CreateUserView.as_view(), name="register-user"),
    # Login
    path("login/", views.LoginView.as_view(), name="user-login"),
    # Logout
    path("logout/", views.LogoutView.as_view(), name="user-logout"),
    # Tokens
    path("verify-otp-token/", views.VerifyOTPView.as_view(), name="token-verification"),
    path("resend-otp/", views.ResendOTPView.as_view(), name="otp-resend"),
    path("token-refresh/", TokenRefreshView.as_view(), name="refresh-tokens"),
    # Password
    path(
        "password/reset/",
        PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "password/reset/confirm/redirect/<str:uidb64>/<str:token>/",
        views.PasswordResetConfirmRedirectView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # Users
    path("users/", views.ListUsersView.as_view(), name="lists-users"),
]
