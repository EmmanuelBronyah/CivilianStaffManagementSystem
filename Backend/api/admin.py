from django.contrib import admin
from .models import CustomUser, Divisions
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# @admin.register(CustomUser)
# class CustomUserAdmin(BaseUserAdmin):
#     list_display = (
#         "username",
#         "fullname",
#         "email",
#         "role",
#         "grade",
#         "division",
#         "is_staff",
#     )
#     search_fields = ("username", "fullname", "email")
#     ordering = ("username",)

#     def save_model(self, request, obj, form, change):
#         """
#         Ensure passwords are hashed when creating or updating users from admin.
#         """
#         if not change or "password" in form.changed_data:
#             obj.set_password(obj.password)  # hash the password before saving
#         super().save_model(request, obj, form, change)


admin.site.register(CustomUser)
admin.site.register(Divisions)
