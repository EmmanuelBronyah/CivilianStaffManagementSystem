from rest_framework import serializers
from . import models
from rest_framework.exceptions import PermissionDenied, ValidationError
from api.models import CustomUser


# TODO: Last name can hold a value decimal value as string. Fix it
# TODO: An empty confirmation date ("") sent from the frontend should be converted to None before saving into database to avoid "Invalid date format error."
# TODO: Ensure that service ids must be digits
# ? GENDER: How can  gender be deleted with it's associated employees even though the gender field in the employee model has a model.PROTECT


class EmployeeWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Employee
        fields = "__all__"
        read_only_fields = ("dob", "station", "category", "probation")

    @staticmethod
    def is_admin_user(request):
        return (
            request.user.is_staff
            and request.user.is_superuser
            and request.user.role == "ADMINISTRATOR"
        )

    @staticmethod
    def is_standard_user(request):
        return request.user.role == "STANDARD USER"

    def update(self, instance, validated_data):
        request = self.context.get("request")
        unrestricted_fields = [
            "unit",
            "structure",
            "blood_group",
            "disable",
            "entry_qualification",
        ]

        is_admin_user = self.is_admin_user(request)
        is_standard_user = self.is_standard_user(request)

        if is_admin_user:
            return super().update(instance, validated_data)

        elif is_standard_user:
            for key in validated_data.keys():
                if key not in unrestricted_fields:
                    raise PermissionDenied(
                        detail=f"You do not have permission to edit the {key} field."
                    )

            return super().update(instance, validated_data)

        else:
            raise PermissionDenied(
                detail=f"You do not have permission to edit employee details."
            )

    @staticmethod
    def validate_name(field, value):
        if not value:
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:
            if char not in VALID_CHARS:
                raise serializers.ValidationError(
                    f"{field} can only contain letters, spaces, hyphens, and periods."
                )
        return value

    def validate_last_name(self, value):
        return self.validate_name("Last Name", value)

    def validate_other_names(self, value):
        return self.validate_name("Other Names", value)

    def validate_social_security(self, value):
        if value is None:
            return value

        if not value.isalnum():
            raise serializers.ValidationError(
                "Field can only contain letters and numbers."
            )

        return value

    def validate(self, attrs):
        social_security = attrs.get("social_security", None)

        if social_security and len(social_security) == 13:
            dob_string = social_security[3:9]
            year, month, day = dob_string[:2], dob_string[2:4], dob_string[4:]

            from datetime import datetime

            try:
                dob = datetime.strptime(f"{year}-{month}-{day}", "%y-%m-%d")
                attrs["dob"] = dob.strftime("%Y-%m-%d")
            except ValueError:
                pass

        return super().validate(attrs)


class EmployeeReadSerializer(serializers.ModelSerializer):
    gender = serializers.StringRelatedField()
    region = serializers.StringRelatedField()
    religion = serializers.StringRelatedField()
    marital_status = serializers.StringRelatedField()
    unit = serializers.StringRelatedField()
    grade = serializers.StringRelatedField()
    structure = serializers.StringRelatedField()
    blood_group = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()

    class Meta:
        model = models.Employee
        fields = "__all__"


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Grades
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Units
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Gender
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


class MaritalStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MaritalStatus
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Region
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


class ReligionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Religion
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


class StructureSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Structure
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


class BloodGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BloodGroup
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


class DocumentFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DocumentFile
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


class UnregisteredEmployeesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UnregisteredEmployees
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation
