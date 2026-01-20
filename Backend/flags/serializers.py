from rest_framework import serializers
from .models import Flags
import logging

logger = logging.getLogger(__name__)


class FlagWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flags
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

    def validate_service_id(self, value):
        if not value:
            logger.debug("Service ID is empty")
            return value

        if not value.isdigit():
            logger.debug("Service ID can only contain numbers.")

            raise serializers.ValidationError("Service ID can only contain numbers.")

        return value

    def validate_field(self, value):
        return self.validate_text("Field", value)

    def validate_reason(self, value):
        return self.validate_text("Reason", value)


class FlagReadSerializer(serializers.ModelSerializer):
    content_type_display = serializers.StringRelatedField(
        source="content_type", read_only=True
    )
    flag_type_display = serializers.StringRelatedField(
        source="flag_type", read_only=True
    )
    created_by_display = serializers.StringRelatedField(
        source="created_by", read_only=True
    )
    updated_by_display = serializers.StringRelatedField(
        source="updated_by", read_only=True
    )
    created_at = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", read_only=True)

    class Meta:
        model = Flags
        fields = "__all__"
