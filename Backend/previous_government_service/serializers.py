from rest_framework import serializers
from .models import PreviousGovernmentService
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
