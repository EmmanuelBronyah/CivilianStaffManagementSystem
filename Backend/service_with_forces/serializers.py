from rest_framework import serializers
from .models import ServiceWithForces, MilitaryRanks, IncompleteServiceWithForcesRecords
import logging

logger = logging.getLogger(__name__)


class ServiceWithForcesWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceWithForces
        fields = "__all__"

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

    def validate_service_date(self, value):
        if not value:
            logger.debug("Service Date is empty")
            return value

        from datetime import datetime

        today = datetime.now().date()
        if value >= today:
            logger.debug("Service Date cannot be the present date or a future date.")

            raise serializers.ValidationError(
                "Service Date cannot be the present date or a future date."
            )

        return value


class ServiceWithForcesReadSerializer(serializers.ModelSerializer):
    military_rank_display = serializers.StringRelatedField(
        source="military_rank", read_only=True
    )
    last_unit_display = serializers.StringRelatedField(
        source="last_unit", read_only=True
    )
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
        model = ServiceWithForces
        fields = "__all__"


class MilitaryRanksSerializer(serializers.ModelSerializer):

    class Meta:
        model = MilitaryRanks
        fields = "__all__"

    @staticmethod
    def validate_text(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {" "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(f"{field} can only contain letters and spaces.")

                raise serializers.ValidationError(
                    f"{field} can only contain letters and spaces."
                )

        return value

    def validate_rank(self, value):
        return self.validate_text("Rank", value)

    def validate_branch(self, value):
        return self.validate_text("Branch", value)


class IncompleteServiceWithForcesRecordsWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncompleteServiceWithForcesRecords
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
                "All fields for Incomplete Service With Forces cannot be empty."
            )

        service_date = attrs.get("service_date")
        service_id = attrs.get("service_id")

        non_service_date_service_id_value = any(
            value not in (None, "")
            for key, value in attrs.items()
            if key not in system_fields | {"service_date", "service_id"}
        )

        if (service_date or service_id) and not non_service_date_service_id_value:
            raise serializers.ValidationError(
                "Cannot save Incomplete Service With Forces with Service Date or Service ID as the only non-empty fields."
            )

        return attrs

    def validate_service_date(self, value):
        if not value:
            logger.debug("Service Date is empty")
            return value

        from datetime import datetime

        today = datetime.now().date()
        if value >= today:
            logger.debug("Service Date cannot be the present date or a future date.")

            raise serializers.ValidationError(
                "Service Date cannot be the present date or a future date."
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

    def validate(self, attrs):
        attrs = self.validate_null_values(attrs)

        return attrs


class IncompleteServiceWithForcesReadSerializer(serializers.ModelSerializer):
    military_rank_display = serializers.StringRelatedField(
        source="military_rank", read_only=True
    )
    last_unit_display = serializers.StringRelatedField(
        source="last_unit", read_only=True
    )
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
        model = IncompleteServiceWithForcesRecords
        fields = "__all__"
