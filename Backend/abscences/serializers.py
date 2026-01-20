from rest_framework import serializers
from .models import Absences
import logging


logger = logging.getLogger(__name__)


class AbsencesWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Absences
        fields = "__all__"

    def validate_absence(self, value):
        if not value:
            logger.debug("Absence is empty")
            return value

        import string

        VALID_CHARS = (
            set(string.ascii_letters) | set(string.digits) | {".", "-", " ", ","}
        )

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Absence can only contain letters, numbers, spaces, hyphens, commas, and periods."
                )

                raise serializers.ValidationError(
                    "Absence can only contain letters, numbers, spaces, hyphens, commas, and periods."
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
        start_date = attrs.get("start_date", None)
        end_date = attrs.get("end_date", None)

        if all([start_date, end_date]):
            logger.debug("Start date and End date both have values")

            if end_date <= start_date:
                logger.debug("End date should be after Start date.")

                raise serializers.ValidationError(
                    "End date should be after Start date."
                )

        return attrs


class AbsencesReadSerializer(serializers.ModelSerializer):
    created_by_display = serializers.StringRelatedField(
        source="created_by", read_only=True
    )
    updated_by_display = serializers.StringRelatedField(
        source="updated_by", read_only=True
    )

    class Meta:
        model = Absences
        fields = "__all__"
