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


class RestrictFields(BasePermission):

    def has_permission(self, request, view):
        restricted_keys = {
            "dob",
            "age",
            "station",
            "category",
            "structure",
            "probation",
        }
        if restricted_keys & set(request.data.keys()):
            self.message = f"The fields ({', '.join(restricted_keys)}) are restricted when creating an Employee record."
            return False

        return True


class CanEditEmployee(BasePermission):

    def has_permission(self, request, view):
        is_admin_user = (
            request.user.is_staff
            and request.user.is_superuser
            and request.user.role == "ADMINISTRATOR"
        )

        if is_admin_user:
            return True

        is_standard_user = request.user.role == "STANDARD USER"

        if is_standard_user:
            restricted_keys = {
                "service_id",
                "dob",
                "age",
                "station",
                "category",
                "structure",
                "probation",
            }
            if restricted_keys & set(request.data.keys()):
                self.message = f"You do not have permission to edit any of these fields: {', '.join(restricted_keys)}"
                return False
            else:
                return True

        return False
