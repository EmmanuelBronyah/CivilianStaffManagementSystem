from rest_framework import serializers
from .models import Spouse
import logging

logger = logging.getLogger(__name__)


class SpouseWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spouse
        fields = "__all__"

    @staticmethod
    def validate_other_text_with_digits(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        import string

        VALID_CHARS = (
            set(string.ascii_letters) | set(string.digits) | {".", "-", " ", ","}
        )

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    f"{field} can only contain letters, numbers, spaces, hyphens, commas, and periods."
                )

                raise serializers.ValidationError(
                    f"{field} can only contain letters, numbers, spaces, hyphens, commas, and periods."
                )

        return value

    def validate_spouse_name(self, value):
        if not value:
            logger.debug("Spouse Name is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Spouse Name can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    "Spouse Name can only contain letters, spaces, hyphens, and periods."
                )

        return value

    def validate_phone_number(self, value):
        if not value:
            logger.debug("Phone Number is empty")
            return value

        if not value.isdigit():
            logger.debug("Phone Number can only contain numbers.")

            raise serializers.ValidationError("Phone Number can only contain numbers.")

        if len(value) < 10 or len(value) > 10:
            logger.debug("Phone Number cannot be lesser or greater than 10 digits.")

            raise serializers.ValidationError(
                "Phone Number cannot be lesser or greater than 10 digits."
            )

        return value

    def validate_address(self, value):
        return self.validate_other_text_with_digits("Address", value)

    def validate_marriage_place(self, value):
        return self.validate_other_text_with_digits("Marriage Place", value)

    def validate_registration_number(self, value):
        return self.validate_other_text_with_digits("Registration Number", value)


class SpouseReadSerializer(serializers.ModelSerializer):
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
        model = Spouse
        fields = "__all__"
