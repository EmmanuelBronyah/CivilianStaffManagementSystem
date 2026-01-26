from rest_framework import serializers
from .models import Identity
import logging
from employees.models import Employee

logger = logging.getLogger(__name__)


class IdentityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = "__all__"

    @staticmethod
    def validate_id(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | set(string.digits) | {"-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    f"{field} can only contain letters, numbers, spaces and hyphens."
                )

                raise serializers.ValidationError(
                    f"{field} can only contain letters, numbers, spaces and hyphens."
                )

        return value

    def validate_voters_id(self, value):
        return self.validate_id("Voters ID", value)

    def validate_national_id(self, value):
        return self.validate_id("National ID", value)

    def validate_glico_id(self, value):
        return self.validate_id("GLICO ID", value)

    def validate_nhis_id(self, value):
        return self.validate_id("NHIS ID", value)

    def validate_tin_number(self, value):
        return self.validate_id("TIN ID", value)

    def validate(self, attrs):
        system_fields = {
            "employee",
            "created_by",
            "updated_by",
            "date_added",
            "date_modified",
        }

        has_value = any(
            value not in (None, "")
            for key, value in attrs.items()
            if key not in system_fields
        )

        if not has_value:
            raise serializers.ValidationError(
                "All fields for Identity cannot be empty."
            )

        return attrs


class IdentityReadSerializer(serializers.ModelSerializer):
    created_by_display = serializers.StringRelatedField(
        source="created_by", read_only=True
    )
    updated_by_display = serializers.StringRelatedField(
        source="updated_by", read_only=True
    )
    date_added = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", read_only=True)
    date_modified = serializers.DateTimeField(
        format="%Y-%m-%d %I:%M %p", read_only=True
    )

    class Meta:
        model = Identity
        fields = "__all__"
