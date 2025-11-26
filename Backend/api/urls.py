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
    path("users/", views.RetrieveAllUsersView.as_view(), name="retrieve-all-users"),
    path(
        "users/<int:pk>/",
        views.RetrieveUserView.as_view(),
        name="retrieve-user",
    ),
    path(
        "users/update/<int:pk>/",
        views.UpdateUserView.as_view(),
        name="update-user",
    ),
    path(
        "users/deactivate/<int:pk>/",
        views.DeactivateUserView.as_view(),
        name="deactivate-user",
    ),
    path(
        "users/restore/<int:pk>/",
        views.RestoreUserAccountView.as_view(),
        name="restore-user-account",
    ),
    path(
        "users/delete/<int:pk>/",
        views.DeleteUserView.as_view(),
        name="delete-user",
    ),
    # Division
    path(
        "divisions/create/",
        views.CreateDivisionAPIView.as_view(),
        name="create-division",
    ),
    path(
        "divisions/",
        views.ListDivisionsAPIView.as_view(),
        name="retrieve-all-divisions",
    ),
    path(
        "divisions/<int:pk>/detail/",
        views.RetrieveDivisionAPIView.as_view(),
        name="retrieve-division",
    ),
    path(
        "divisions/<int:pk>/update/",
        views.EditDivisionAPIView.as_view(),
        name="update-division",
    ),
    path(
        "divisions/<int:pk>/delete/",
        views.DeleteDivisionAPIView.as_view(),
        name="delete-division",
    ),
]
