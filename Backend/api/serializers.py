from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import Group
import logging
from . import models


logger = logging.getLogger(__name__)


class RetrieveCreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        value = value.strip().lower()
        if not serializers.EmailField().run_validation(value):
            raise serializers.ValidationError("Enter a valid email address.")

        return value

    def create(self, validated_data):
        user = CustomUser(
            fullname=validated_data["fullname"],
            username=validated_data["username"],
            email=validated_data["email"],
            grade=validated_data["grade"],
            division=validated_data["division"],
            role=validated_data["role"],
            created_by=validated_data["created_by"],
            updated_by=validated_data["updated_by"],
        )
        user.set_password(validated_data["password"])
        logger.debug(f"User({user}) password has been set.")

        group = Group.objects.get(name__iexact=validated_data["role"])
        logger.debug(f"User({user}) group({group}).")

        if group.name.lower() == "administrator":
            user.is_superuser, user.is_staff = True, True

        user.save()
        logger.debug(f"User({user}) has been saved.")

        user.groups.add(group)
        logger.debug(f"User({user}) added to group({group}).")

        return user


class RetrieveUpdateDestroyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        admin_group_id, standard_user_group_id, viewer_group_id = 1, 3, 2

        if "role" in list(validated_data.keys()):
            role = validated_data.get("role")

            if role.lower() == "administrator":
                instance.groups.clear()
                instance.groups.add(admin_group_id)
                instance.is_superuser, instance.is_staff = True, True
                instance.save()

            elif role.lower() == "standard user" or role.lower() == "viewer":
                instance.groups.clear()
                instance.groups.add(
                    viewer_group_id
                    if role.lower() == "viewer"
                    else standard_user_group_id
                )
                instance.is_superuser, instance.is_staff = False, False
                instance.save()

            return instance

        else:
            return super().update(instance, validated_data)


class UserReadSerializer(serializers.ModelSerializer):
    grade_display = serializers.StringRelatedField(source="grade", read_only=True)
    division_display = serializers.StringRelatedField(source="division", read_only=True)
    created_by_display = serializers.StringRelatedField(
        source="created_by", read_only=True
    )
    updated_by_display = serializers.StringRelatedField(
        source="updated_by", read_only=True
    )
    created_at = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "fullname",
            "role",
            "email",
            "grade",
            "division",
            "created_by",
            "updated_by",
            "grade_display",
            "division_display",
            "created_by_display",
            "updated_by_display",
            "created_at",
            "updated_at",
        )


class DivisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Divisions
        fields = "__all__"

    def validate_division_name(self, value):
        if not value:
            logger.debug("Division is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {"-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug("Division can only contain letters, spaces and hyphens.")

                raise serializers.ValidationError(
                    "Division can only contain letters, spaces and hyphens."
                )

        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class VerifyOTPSerializer(serializers.Serializer):
    tokens = serializers.JSONField()

    def validate(self, data):
        tokens = data["tokens"]
        invalid_keys = [key for key in tokens if key not in ["temp_token", "otp_token"]]
        logger.debug(f"Invalid keys ({invalid_keys}).")

        for key in invalid_keys:
            del tokens[key]
        return data
