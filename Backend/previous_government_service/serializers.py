from rest_framework import serializers
from .models import (
    PreviousGovernmentService,
    IncompletePreviousGovernmentServiceRecords,
)
import logging


logger = logging.getLogger(__name__)


class PreviousGovernmentServiceWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreviousGovernmentService
        fields = "__all__"

    @staticmethod
    def validate_text(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " ", ","}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    f"{field} can only contain letters, spaces, hyphens, commas, and periods."
                )

                raise serializers.ValidationError(
                    f"{field} can only contain letters, spaces, hyphens, commas, and periods."
                )

        return value

    def validate_institution(self, value):
        return self.validate_text("Institution", value)

    def validate_position(self, value):
        return self.validate_text("Position", value)

    def validate_duration(self, value):
        if not value:
            logger.debug("Duration is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | set(string.digits) | {" "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug("Duration can only contain letters, numbers and spaces.")

                raise serializers.ValidationError(
                    "Duration can only contain letters, numbers and spaces."
                )

        return value

    def validate(self, attrs):
        start_date = attrs.get("start_date", None)
        end_date = attrs.get("end_date", None)

        if start_date and end_date:
            if end_date <= start_date:
                logger.debug("End date should be after Start date.")

                raise serializers.ValidationError(
                    "End date should be after Start date."
                )

        return attrs


class PreviousGovernmentServiceReadSerializer(serializers.ModelSerializer):
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
        model = PreviousGovernmentService
        fields = "__all__"


class IncompletePreviousGovernmentServiceWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncompletePreviousGovernmentServiceRecords
        fields = "__all__"

    @staticmethod
    def validate_text(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " ", ","}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    f"{field} can only contain letters, spaces, hyphens, commas, and periods."
                )

                raise serializers.ValidationError(
                    f"{field} can only contain letters, spaces, hyphens, commas, and periods."
                )

        return value

    @staticmethod
    def validate_dates(attrs):
        start_date = attrs.get("start_date", None)
        end_date = attrs.get("end_date", None)

        if start_date and end_date:
            if end_date <= start_date:
                logger.debug("End date should be after Start date.")

                raise serializers.ValidationError(
                    "End date should be after Start date."
                )

        return attrs

    @staticmethod
    def validate_null_values(attrs):
        system_fields = {"created_by", "updated_by", "employee"}

        has_value = any(
            value not in (None, "")
            for key, value in attrs.items()
            if key not in system_fields
        )

        if not has_value:
            raise serializers.ValidationError(
                "All fields for Incomplete Previous Government Service cannot be empty."
            )

        duration = attrs.get("duration")
        service_id = attrs.get("service_id")

        non_duration_service_id_value = any(
            value not in (None, "")
            for key, value in attrs.items()
            if key not in system_fields | {"duration", "service_id"}
        )

        if (duration or service_id) and not non_duration_service_id_value:
            raise serializers.ValidationError(
                "Cannot save Incomplete Previous Government Service with Duration or Service ID as the only non-empty fields."
            )

        return attrs

    def validate_institution(self, value):
        return self.validate_text("Institution", value)

    def validate_position(self, value):
        return self.validate_text("Position", value)

    def validate_service_id(self, value):
        if not value:
            logger.debug("Service ID is empty")
            return value

        if not value.isdigit():
            logger.debug("Service ID can only contain numbers.")

            raise serializers.ValidationError("Field can only contain numbers.")

        if len(value) < 5:
            logger.debug("Service ID must have more than five(5) digits.")

            raise serializers.ValidationError(
                "Service ID must have more than five(5) digits."
            )

        return value

    def validate_duration(self, value):
        if not value:
            logger.debug("Duration is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | set(string.digits) | {" "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug("Duration can only contain letters, numbers and spaces.")

                raise serializers.ValidationError(
                    "Duration can only contain letters, numbers and spaces."
                )

        return value

    def validate(self, attrs):
        attrs = self.validate_dates(attrs)

        attrs = self.validate_null_values(attrs)

        return attrs


class IncompletePreviousGovernmentServiceReadSerializer(serializers.ModelSerializer):
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
        model = IncompletePreviousGovernmentServiceRecords
        fields = "__all__"
