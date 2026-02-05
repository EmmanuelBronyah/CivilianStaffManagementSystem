from rest_framework import serializers
from .models import (
    Occurrence,
    LevelStep,
    SalaryAdjustmentPercentage,
    Event,
    IncompleteOccurrence,
)
import logging
from .utils import two_dp


logger = logging.getLogger(__name__)


class BaseOccurrenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Occurrence
        fields = "__all__"

    def validate_wef_date(self, value):
        if not value:
            logger.debug("Wef Date is empty")
            return value

        from datetime import datetime

        today = datetime.now().date()

        if value >= today:
            logger.debug("Wef Date cannot be a future date.")

            raise serializers.ValidationError("Wef Date cannot be a future date.")

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

    def validate_reason(self, value):
        if not value:
            logger.debug("Reason is empty")
            return value

        import string

        VALID_CHARS = (
            set(string.ascii_letters) | set(string.digits) | {".", "-", " ", ",", "%"}
        )

        for char in value:

            if char not in VALID_CHARS:
                logger.debug(
                    "Reason can only contain letters, numbers, spaces, hyphens, commas, periods and the percentage sign (%)."
                )

                raise serializers.ValidationError(
                    "Reason can only contain letters, numbers, spaces, hyphens, commas, periods and the percentage sign (%)."
                )

        return value


class OccurrenceWriteSerializer(BaseOccurrenceSerializer):
    percentage_adjustment = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Occurrence
        exclude = ("monthly_salary", "annual_salary")

    def assign_annual_salary(self, attrs):
        event = attrs.get("event", None)
        event = event.event_name

        level_step = attrs.get("level_step", None)
        monthly_salary = level_step.monthly_salary
        monthly_salary = two_dp(monthly_salary)

        if event != "Salary Adjustment":
            # Remove percentage_adjustment key
            attrs.pop("percentage_adjustment")

            attrs["monthly_salary"] = str(monthly_salary)

            annual_salary = two_dp(two_dp(12) * monthly_salary)
            attrs["annual_salary"] = str(annual_salary)

        else:
            percentage_adjustment = attrs.pop("percentage_adjustment")
            percentage_adjustment = two_dp(two_dp(percentage_adjustment) / two_dp(100))

            monthly_salary = two_dp(
                (two_dp(monthly_salary * percentage_adjustment)) + monthly_salary
            )
            attrs["monthly_salary"] = str(monthly_salary)

            annual_salary = two_dp(two_dp(12) * monthly_salary)
            attrs["annual_salary"] = str(annual_salary)

        return attrs

    def validate(self, attrs):
        attrs = self.assign_annual_salary(attrs)

        return attrs


class OccurrenceUpdateSerializer(BaseOccurrenceSerializer):

    class Meta(BaseOccurrenceSerializer.Meta):
        pass


class OccurrenceReadSerializer(serializers.ModelSerializer):
    grade_display = serializers.StringRelatedField(source="grade", read_only=True)
    level_step_display = serializers.StringRelatedField(
        source="level_step", read_only=True
    )
    event_display = serializers.StringRelatedField(source="event", read_only=True)
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
        model = Occurrence
        fields = "__all__"


class LevelStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = LevelStep
        fields = "__all__"

    def validate_level_step(self, value):
        if not value:
            logger.debug("Level|Step is empty")
            return value

        if not value.isalnum():
            logger.debug("Level|Step can only contain letters and numbers.")

            raise serializers.ValidationError(
                "Level|Step can only contain letters and numbers."
            )

        return value

    def validate_monthly_salary(self, value):
        minimum_salary = two_dp(1000)
        salary_provided = two_dp(value)

        if salary_provided <= minimum_salary:
            logger.debug("Salary cannot be lesser than 1000.00")

            raise serializers.ValidationError("Salary cannot be lesser than 1000.00")

        return value


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"

    def validate_event_name(self, value):
        if not value:
            logger.debug("Event is empty")
            return value

        import string

        VALID_CHARS = set(string.ascii_letters) | {" "}

        for char in value:

            if char not in VALID_CHARS:
                logger.debug("Event can only contain letters and spaces.")

                raise serializers.ValidationError(
                    "Event can only contain letters and spaces."
                )

        return value


class SalaryAdjustmentPercentageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalaryAdjustmentPercentage
        fields = "__all__"


class IncompleteOccurrenceWriteSerializer(BaseOccurrenceSerializer):
    percentage_adjustment = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = IncompleteOccurrence
        exclude = ("monthly_salary", "annual_salary")

    def assign_annual_salary(self, attrs):
        event = attrs.get("event", None)
        event = event.event_name

        level_step = attrs.get("level_step", None)
        monthly_salary = level_step.monthly_salary
        monthly_salary = two_dp(monthly_salary)

        if event != "Salary Adjustment":
            # Remove percentage_adjustment key
            attrs.pop("percentage_adjustment")

            attrs["monthly_salary"] = str(monthly_salary)

            annual_salary = two_dp(two_dp(12) * monthly_salary)
            attrs["annual_salary"] = str(annual_salary)

        else:
            percentage_adjustment = attrs.pop("percentage_adjustment")
            percentage_adjustment = two_dp(two_dp(percentage_adjustment) / two_dp(100))

            monthly_salary = two_dp(
                (two_dp(monthly_salary * percentage_adjustment)) + monthly_salary
            )
            attrs["monthly_salary"] = str(monthly_salary)

            annual_salary = two_dp(two_dp(12) * monthly_salary)
            attrs["annual_salary"] = str(annual_salary)

        return attrs

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
        attrs = self.assign_annual_salary(attrs)

        return attrs


class IncompleteOccurrenceUpdateSerializer(BaseOccurrenceSerializer):

    class Meta:
        model = IncompleteOccurrence
        fields = "__all__"

    def validate_service_id(self, value):
        if not value:
            logger.debug("Service ID is empty")
            return value

        if not value.isdigit():
            logger.debug("Service ID can only contain numbers.")

            raise serializers.ValidationError("Service ID can only contain numbers.")

        return value


class IncompleteOccurrenceReadSerializer(serializers.ModelSerializer):
    grade_display = serializers.StringRelatedField(source="grade", read_only=True)
    level_step_display = serializers.StringRelatedField(
        source="level_step", read_only=True
    )
    event_display = serializers.StringRelatedField(source="event", read_only=True)
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
        model = IncompleteOccurrence
        fields = "__all__"
