from rest_framework import serializers
from .models import CustomUser, Divisions
from employees.models import Grades
from django.contrib.auth.models import Group
import logging
from . import models


logger = logging.getLogger(__name__)


class RetrieveCreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate_user_email(self, value):
        value = value.strip().lower()
        if not serializers.EmailField().run_validation(value):
            raise serializers.ValidationError("Enter a valid email address.")

        return value

    def create(self, validated_data):
        user = CustomUser(
            fullname=validated_data["fullname"],
            username=validated_data["username"],
            user_email=validated_data["user_email"],
            grade=validated_data["grade"],
            division=validated_data["division"],
            role=validated_data["role"],
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        division_id = representation.pop("division", None)
        division_name = Divisions.objects.get(id=division_id).division_name

        grade_id = representation.pop("grade", None)
        grade_name = Grades.objects.get(id=grade_id).grade_name

        representation.pop("id", None)
        representation.pop("password", None)
        representation.pop("first_name", None)
        representation.pop("last_name", None)
        representation.pop("last_login", None)
        representation.pop("is_superuser", None)
        representation.pop("is_staff", None)
        representation.pop("date_joined", None)
        representation.pop("groups", None)
        representation.pop("user_permissions", None)

        representation.update({"grade": grade_name})
        representation.update({"division": division_name})

        return representation


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        division_id = representation.pop("division", None)
        division_name = Divisions.objects.get(id=division_id).division_name

        grade_id = representation.pop("grade", None)
        grade_name = Grades.objects.get(id=grade_id).grade_name

        representation.pop("id", None)
        representation.pop("password", None)
        representation.pop("first_name", None)
        representation.pop("last_name", None)
        representation.pop("last_login", None)
        representation.pop("is_superuser", None)
        representation.pop("is_staff", None)
        representation.pop("date_joined", None)
        representation.pop("groups", None)
        representation.pop("user_permissions", None)

        representation.update({"grade": grade_name})
        representation.update({"division": division_name})

        return representation


class DivisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Divisions
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


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
