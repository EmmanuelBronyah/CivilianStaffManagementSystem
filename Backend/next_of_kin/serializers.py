from rest_framework import serializers
from .models import EmergencyOrNextOfKin
import logging

logger = logging.getLogger(__name__)


class EmergencyOrNextOfKinWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmergencyOrNextOfKin
        fields = "__all__"

    @staticmethod
    def validate_contact(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        if not value.isdigit():
            logger.debug(f"{field} can only contain numbers.")

            raise serializers.ValidationError(f"{field} can only contain numbers.")

        if len(value) < 10 or len(value) > 10:
            logger.debug(f"{field} cannot be lesser or greater than 10 digits.")

            raise serializers.ValidationError(
                f"{field} cannot be lesser or greater than 10 digits."
            )

        return value

    def validate_address(self, value):
        if not value:
            logger.debug("Address is empty")
            return value

        import string

        VALID_CHARS = (
            set(string.ascii_letters) | set(string.digits) | {".", "-", " ", ","}
        )

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Address can only contain letters, numbers, spaces, hyphens, commas, and periods."
                )

                raise serializers.ValidationError(
                    "Address can only contain letters, numbers, spaces, hyphens, commas, and periods."
                )

        return value

    def validate_phone_number(self, value):
        return self.validate_contact("Phone Number", value)

    def validate_emergency_contact(self, value):
        return self.validate_contact("Emergency Contact", value)

    def validate_name(self, value):
        if not value:
            logger.debug("Name is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Name can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "Name can only contain letters, spaces, hyphens, and periods."
                )

        return value

    def validate_relation(self, value):
        if not value:
            logger.debug("Relation is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {"-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug("Relation can only contain letters, spaces and hyphens.")

                raise serializers.ValidationError(
                    "Relation can only contain letters, spaces and hyphens."
                )

        return value


class EmergencyOrNextOfKinReadSerializer(serializers.ModelSerializer):
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
        model = EmergencyOrNextOfKin
        fields = "__all__"
