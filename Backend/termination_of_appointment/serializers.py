from rest_framework import serializers
from . import models
import logging

logger = logging.getLogger(__name__)


class TerminationOfAppointmentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TerminationOfAppointment
        fields = "__all__"

    def validate_date(self, value):
        if not value:
            logger.debug("Date is empty")
            return value

        from datetime import datetime

        today = datetime.now().date()
        if value >= today:
            logger.debug("Date cannot be the present date or a future date.")

            raise serializers.ValidationError(
                "Date cannot be the present date or a future date."
            )

        return value

    def validate_authority(self, value):
        if not value:
            logger.debug("Authority is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | set(string.digits) | {"/", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Authority can only contain letters, numbers, and a forward slash (/)."
                )

                raise serializers.ValidationError(
                    "Authority can only contain letters, numbers, and a forward slash (/)."
                )

        return value


class TerminationOfAppointmentReadSerializer(serializers.ModelSerializer):
    cause_display = serializers.StringRelatedField(source="cause", read_only=True)
    status_display = serializers.StringRelatedField(source="status", read_only=True)
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
        model = models.TerminationOfAppointment
        fields = "__all__"


class CausesOfTerminationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CausesOfTermination
        fields = "__all__"

    def validate_termination_cause(field, value):
        if not value:
            logger.debug("Cause is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {" "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug("Cause can only contain letters and spaces.")

                raise serializers.ValidationError(
                    "Cause can only contain letters and spaces."
                )

        return value


class TerminationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TerminationStatus
        fields = "__all__"

    def validate_termination_status(field, value):
        if not value:
            logger.debug("Status is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {" "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug("Status can only contain letters and spaces.")

                raise serializers.ValidationError(
                    "Status can only contain letters and spaces."
                )

        return value


class IncompleteTerminationOfAppointmentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IncompleteTerminationOfAppointmentRecords
        fields = "__all__"

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
                "All fields for Incomplete Termination of Appointment cannot be empty."
            )

        date = attrs.get("date")
        service_id = attrs.get("service_id")

        non_date_service_id_value = any(
            value not in (None, "")
            for key, value in attrs.items()
            if key not in system_fields | {"date", "service_id"}
        )

        if (date or service_id) and not non_date_service_id_value:
            raise serializers.ValidationError(
                "Cannot save Incomplete Termination of Appointment with Date or Service ID as the only non-empty fields."
            )

        return attrs

    def validate_date(self, value):
        if not value:
            logger.debug("Date is empty")
            return value

        from datetime import datetime

        today = datetime.now().date()
        if value >= today:
            logger.debug("Date cannot be the present date or a future date.")

            raise serializers.ValidationError(
                "Date cannot be the present date or a future date."
            )

        return value

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

    def validate_authority(self, value):
        if not value:
            logger.debug("Authority is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | set(string.digits) | {"/", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Authority can only contain letters, numbers, and a forward slash (/)."
                )

                raise serializers.ValidationError(
                    "Authority can only contain letters, numbers, and a forward slash (/)."
                )

        return value

    def validate(self, attrs):
        attrs = self.validate_null_values(attrs)

        return attrs


class IncompleteTerminationOfAppointmentReadSerializer(serializers.ModelSerializer):
    cause_display = serializers.StringRelatedField(source="cause", read_only=True)
    status_display = serializers.StringRelatedField(source="status", read_only=True)
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
        model = models.IncompleteTerminationOfAppointmentRecords
        fields = "__all__"
