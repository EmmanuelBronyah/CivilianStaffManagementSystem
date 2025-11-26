from rest_framework import serializers
from . import models
from rest_framework.exceptions import PermissionDenied, ValidationError


# TODO: Last name can hold a value decimal value as string. Fix it
# TODO: An empty confirmation date ("") sent from the frontend should be converted to None before saving into database to avoid "Invalid date format error."
# ? GENDER: How can  gender be deleted with it's associated employees even though the gender field in the employee model has a model.PROTECT


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Employee
        fields = "__all__"

    def update(self, instance, validated_data):
        request = self.context.get("request")
        unrestricted_fields = [
            "unit",
            "structure",
            "blood_group",
            "disable",
            "entry_qualification",
        ]

        is_admin_user = (
            request.user.is_staff
            and request.user.is_superuser
            and request.user.role == "ADMINISTRATOR"
        )
        is_standard_user = request.user.role == "STANDARD USER"

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

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop("id", None)
    #     return representation


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
