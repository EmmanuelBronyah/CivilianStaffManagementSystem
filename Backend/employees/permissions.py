from rest_framework.permissions import BasePermission


class IsAdminUserOrStandardUser(BasePermission):

    def has_permission(self, request, view):
        is_admin_user = (
            request.user.is_staff
            and request.user.is_superuser
            and request.user.role == "ADMINISTRATOR"
        )
        is_standard_user = request.user.role == "STANDARD USER"

        return (is_admin_user) or is_standard_user
