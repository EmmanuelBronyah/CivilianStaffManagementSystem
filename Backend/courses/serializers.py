from rest_framework import serializers
from .models import Courses, IncompleteCourseRecords
import logging

logger = logging.getLogger(__name__)


# todo: make sure edit requests with partial edit data are able to edit successfully
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


class IncompleteCourseRecordsWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncompleteCourseRecords
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
                "All fields for Incomplete Course Record cannot be empty."
            )

        authority = attrs.get("authority")
        result = attrs.get("result")
        service_id = attrs.get("service_id")

        non_authority_result_service_id_value = any(
            value not in (None, "")
            for key, value in attrs.items()
            if key not in system_fields | {"authority", "result", "service_id"}
        )

        if (
            authority or service_id or result
        ) and not non_authority_result_service_id_value:
            raise serializers.ValidationError(
                "Cannot save Incomplete Course Record with Result/Authority/Service ID as the only non-empty fields."
            )

        return attrs

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

    def validate_service_id(self, value):
        if not value:
            logger.debug("Service ID is empty")
            return value

        if not value.isdigit():
            logger.debug("Service ID can only contain numbers.")

            raise serializers.ValidationError("Field can only contain numbers.")

        return value

    def validate(self, attrs):
        attrs = self.validate_dates(attrs)

        attrs = self.validate_null_values(attrs)

        return attrs


class IncompleteCourseRecordsReadSerializer(serializers.ModelSerializer):
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
        model = IncompleteCourseRecords
        fields = "__all__"
