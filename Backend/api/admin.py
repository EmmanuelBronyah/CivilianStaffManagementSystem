from django.contrib import admin
from .models import CustomUser, Divisions
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.register(CustomUser)
admin.site.register(Divisions)
