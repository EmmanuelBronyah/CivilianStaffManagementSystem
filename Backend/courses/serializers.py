from rest_framework import serializers
from .models import Courses
import logging

logger = logging.getLogger(__name__)


class CoursesWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courses
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

    def validate_course_type(self, value):
        if not value:
            logger.debug("Course Type is empty")
            return value

        import string

        VALID_CHARS = (
            set(string.ascii_letters) | set(string.digits) | {".", "-", " ", ","}
        )

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Course Type can only contain letters, numbers, spaces, hyphens, commas, and periods."
                )

                raise serializers.ValidationError(
                    "Course Type can only contain letters, numbers, spaces, hyphens, commas, and periods."
                )

        return value

    def validate_place(self, value):
        return self.validate_text("Place", value)

    def validate_qualification(self, value):
        return self.validate_text("Qualification", value)

    def validate_result(self, value):
        return self.validate_text("Result", value)

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
        date_commenced = attrs.get("date_commenced", None)
        date_ended = attrs.get("date_ended", None)

        if all([date_commenced, date_ended]):
            logger.debug("Date Commenced and Date Ended both have values")

            if date_ended <= date_commenced:
                logger.debug("Date Ended should be after Date Commenced.")

                raise serializers.ValidationError(
                    "Date Ended should be after Date Commenced."
                )

        return attrs


class CoursesReadSerializer(serializers.ModelSerializer):
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
        model = Courses
        fields = "__all__"
