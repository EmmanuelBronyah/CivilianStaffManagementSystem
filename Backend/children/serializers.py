from rest_framework import serializers
from .models import Children
import logging


logger = logging.getLogger(__name__)


class ChildrenWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Children
        fields = "__all__"

    @staticmethod
    def validate_name(field, value):
        if not value:
            logger.debug(f"{field} is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {".", "-", " "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    f"{field} can only contain letters, spaces, hyphens, and periods."
                )

                raise serializers.ValidationError(
                    f"{field} can only contain letters, spaces, hyphens, and periods."
                )

        return value

    def validate_child_name(self, value):
        return self.validate_name("Child Name", value)

    def validate_other_parent(self, value):
        return self.validate_name("Other Parent", value)

    def validate_dob(self, value):
        if not value:
            logger.debug("Date of Birth is empty")
            return value

        from datetime import datetime

        today = datetime.now().date()

        if value >= today:
            logger.debug("DOB cannot be a future date.")

            raise serializers.ValidationError("Date of Birth cannot be a future date.")

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


class ChildrenReadSerializer(serializers.ModelSerializer):
    created_by_display = serializers.StringRelatedField(
        source="created_by", read_only=True
    )
    updated_by_display = serializers.StringRelatedField(
        source="updated_by", read_only=True
    )
    gender_display = serializers.StringRelatedField(source="gender", read_only=True)
    date_added = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", read_only=True)
    date_modified = serializers.DateTimeField(
        format="%Y-%m-%d %I:%M %p", read_only=True
    )

    class Meta:
        model = Children
        fields = "__all__"
