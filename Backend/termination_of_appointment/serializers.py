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

            serializers.ValidationError(
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
