from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import Group
import logging


logger = logging.getLogger(__name__)


class ListCreateUserSerializer(serializers.ModelSerializer):

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
        )
        user.set_password(validated_data["password"])
        logger.debug(f"User({user}) password has been set.")
        user.save()
        logger.debug(f"User({user}) has been saved.")

        group = Group.objects.get(name__iexact=validated_data["role"])
        logger.debug(f"User({user}) group({group}).")
        user.groups.add(group)
        logger.debug(f"User({user}) added to group({group}).")

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("id", None)
        representation.pop("first_name", None)
        representation.pop("last_name", None)
        representation.pop("last_login", None)
        representation.pop("is_superuser", None)
        representation.pop("is_staff", None)
        representation.pop("is_active", None)
        representation.pop("date_joined", None)
        representation.pop("groups", None)
        representation.pop("user_permissions", None)

        return representation


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
