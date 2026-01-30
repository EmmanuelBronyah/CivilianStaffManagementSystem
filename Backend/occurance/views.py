from rest_framework import generics
from .models import (
    Occurrence,
    LevelStep,
    SalaryAdjustmentPercentage,
    Event,
    IncompleteOccurrence,
)
from . import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from employees.permissions import IsAdminUserOrStandardUser
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
from activity_feeds.models import ActivityFeeds
import logging
from .utils import occurrence_changes, level_step_changes, incomplete_occurrence_changes
from employees.models import Employee
from django.shortcuts import get_object_or_404
from .utils import two_dp
from django.db.models import IntegerField, Value
from django.db.models.functions import Cast, Substr, StrIndex
from flags.services import create_flag, delete_flag
from employees.views import LargeResultsSetPagination
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


logger = logging.getLogger(__name__)


# * OCCURRENCE
class CreateOccurrenceAPIView(generics.CreateAPIView):
    queryset = Occurrence.objects.all()
    serializer_class = serializers.OccurrenceWriteSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        occurrence_data = request.data
        is_many = isinstance(occurrence_data, list)

        serializer = self.get_serializer(data=occurrence_data, many=is_many)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.OccurrenceReadSerializer(
            self.occurrence, many=is_many
        )

        return Response(read_serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        with transaction.atomic():
            self.occurrence = serializer.save(
                created_by=self.request.user, updated_by=self.request.user
            )
            records = (
                ", ".join([str(record) for record in self.occurrence])
                if isinstance(self.occurrence, list)
                else self.occurrence
            )
            logger.debug(f"Occurrence({records}) created.")

            if isinstance(self.occurrence, list):
                for record in self.occurrence:
                    ActivityFeeds.objects.create(
                        creator=self.request.user,
                        activity=(
                            f"{self.request.user} added a new Occurrence(Service ID: {record.employee.service_id} — Authority: {record.authority} — Event: {record.event})"
                        ),
                    )
                    logger.debug(
                        f"Activity Feed({self.request.user} added a new Occurrence(Service ID: {record.employee.service_id} — Authority: {record.authority} — Event: {record.event}) created."
                    )
            else:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=(
                        f"{self.request.user} added a new Occurrence(Service ID: {self.occurrence.employee.service_id} — Authority: {self.occurrence.authority} — Event: {self.occurrence.event})"
                    ),
                )
                logger.debug(
                    f"Activity Feed({self.request.user} added a new Occurrence(Service ID: {self.occurrence.employee.service_id} — Authority: {self.occurrence.authority} — Event: {self.occurrence.event}) created."
                )


class EditOccurrenceAPIView(generics.UpdateAPIView):
    queryset = Occurrence.objects.all()
    serializer_class = serializers.OccurrenceUpdateSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.OccurrenceReadSerializer(self.occurrence_update)

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        with transaction.atomic():
            previous_occurrence = self.get_object()
            self.occurrence_update = serializer.save(updated_by=self.request.user)
            logger.debug(f"Occurrence({previous_occurrence}) updated.")

            changes = occurrence_changes(previous_occurrence, self.occurrence_update)

            if changes:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=f"{self.request.user} updated Occurrence(Service ID: {previous_occurrence.employee.service_id} — Authority: {previous_occurrence.authority} — Event: {previous_occurrence.event}): {changes}",
                )
                logger.debug(
                    f"Activity feed({self.request.user} updated Occurrence(Service ID: {previous_occurrence.employee.service_id} — Authority: {previous_occurrence.authority} — Event: {previous_occurrence.event}): {changes})) created."
                )


class ListEmployeeOccurrenceAPIView(generics.ListAPIView):
    serializer_class = serializers.OccurrenceReadSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        occurrences = (
            employee.occurrences.select_related(
                "created_by", "updated_by", "grade", "level_step", "event"
            )
            .annotate(
                serial_number=Cast(
                    Substr("authority", 5, StrIndex("authority", Value("/")) - 5),
                    IntegerField(),
                )
            )
            .order_by("-serial_number")
        )

        return occurrences


class DeleteOccurrenceAPIView(generics.DestroyAPIView):
    queryset = Occurrence.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.OccurrenceWriteSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.delete()
            logger.debug(f"Occurrence({instance}) deleted.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"The Occurrence(Service ID: {instance.employee.service_id} — Authority: {instance.authority} — Event: {instance.event}) was deleted by {self.request.user}",
            )
            logger.debug(
                f"Activity feed(The Occurrence(Service ID: {instance.employee.service_id} — Authority: {instance.authority} — Event: {instance.event})) created."
            )


# * LEVEL|STEP
class CreateLevelStepAPIView(generics.CreateAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializers.LevelStepSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        with transaction.atomic():
            level_step = serializer.save()
            logger.debug(f"Level|Step({level_step}) created.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=(
                    f"{self.request.user} added a new Level|Step(Level|Step: {level_step.level_step} — Monthly Salary: {level_step.monthly_salary})"
                ),
            )
            logger.debug(
                f"Activity Feed({self.request.user} added a new Level|Step(Level|Step: {level_step.level_step} — Monthly Salary: {level_step.monthly_salary})) created."
            )


class EditLevelStepAPIView(generics.UpdateAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializers.LevelStepSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        with transaction.atomic():
            previous_level_step = self.get_object()
            level_step_update = serializer.save()
            logger.debug(f"Level|Step({previous_level_step}) updated.")

            changes = level_step_changes(previous_level_step, level_step_update)

            if changes:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=f"{self.request.user} updated Level|Step(Level|Step: {previous_level_step.level_step} — Monthly Salary: {previous_level_step.monthly_salary}): {changes}",
                )
                logger.debug(
                    f"Activity Feed({self.request.user} updated Level|Step(Level|Step: {previous_level_step.level_step} — Monthly Salary: {previous_level_step.monthly_salary}): {changes}) created."
                )


class ListLevelStepAPIView(generics.ListAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializers.LevelStepSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class RetrieveLevelStepAPIView(generics.RetrieveAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializers.LevelStepSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class DeleteLevelStepAPIView(generics.DestroyAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializers.LevelStepSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.delete()
            logger.debug(f"Level|Step({instance}) deleted.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"The Level|Step(Level|Step: {instance.level_step} — Monthly Salary: {instance.monthly_salary}) was deleted by {self.request.user}",
            )
            logger.debug(
                f"Activity feed(The Level|Step(Level|Step: {instance.level_step} — Monthly Salary: {instance.monthly_salary}) was deleted by {self.request.user}) created."
            )


class CalculateAnnualSalary(generics.RetrieveAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializers.LevelStepSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        annual_salary = two_dp(two_dp(data["monthly_salary"]) * two_dp(12))
        data.update(annual_salary=annual_salary)
        return Response(data)


# * EVENT
class CreateEventAPIView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        with transaction.atomic():
            event = serializer.save()
            logger.debug(f"Event({event}) created.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=(f"{self.request.user} added a new Event({event.event_name})"),
            )
            logger.debug(
                f"Activity Feed({self.request.user} added a new Event({event.event_name})) created."
            )


class EditEventAPIView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        with transaction.atomic():
            previous_event = self.get_object()
            event_update = serializer.save()
            logger.debug(f"Event({previous_event}) updated.")

            is_changed = previous_event.event_name != event_update.event_name
            if is_changed:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=f"{self.request.user} updated Event({previous_event.event_name}): Event: {previous_event.event_name} → {event_update.event_name}",
                )
                logger.debug(
                    f"Activity Feed({self.request.user} updated Event({previous_event.event_name}): Event: {previous_event.event_name} → {event_update.event_name}) created."
                )


class ListEventAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class RetrieveEventAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class DeleteEventAPIView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.delete()
            logger.debug(f"Event({instance}) deleted.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"The Event({instance.event_name}) was deleted by {self.request.user}",
            )
            logger.debug(
                f"Activity feed(The Event({instance.event_name}) was deleted by {self.request.user}) created."
            )


# * SALARY PERCENTAGE ADJUSTMENT
class CreateSalaryAdjustmentPercentageAPIView(generics.CreateAPIView):
    queryset = SalaryAdjustmentPercentage.objects.all()
    serializer_class = serializers.SalaryAdjustmentPercentageSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        with transaction.atomic():
            salary_adjustment_percentage = serializer.save()
            logger.debug(
                f"Salary Adjustment Percentage({salary_adjustment_percentage}) created."
            )

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=(
                    f"{self.request.user} added a new Salary Adjustment Percentage({salary_adjustment_percentage.percentage_adjustment}%)"
                ),
            )
            logger.debug(
                f"Activity Feed({self.request.user} added a new Salary Adjustment Percentage({salary_adjustment_percentage.percentage_adjustment}%)) created."
            )


class EditSalaryAdjustmentPercentageAPIView(generics.UpdateAPIView):
    queryset = SalaryAdjustmentPercentage.objects.all()
    serializer_class = serializers.SalaryAdjustmentPercentageSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        with transaction.atomic():
            previous_salary_adjustment_percentage = self.get_object()
            salary_adjustment_percentage_update = serializer.save()
            logger.debug(
                f"Salary Percentage Adjustment({previous_salary_adjustment_percentage}) updated."
            )

            is_changed = (
                previous_salary_adjustment_percentage.percentage_adjustment
                != salary_adjustment_percentage_update.percentage_adjustment
            )
            if is_changed:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=f"{self.request.user} updated Salary Percentage Adjustment({previous_salary_adjustment_percentage.percentage_adjustment}): Percentage Adjustment: {previous_salary_adjustment_percentage.percentage_adjustment}% → {salary_adjustment_percentage_update.percentage_adjustment}%",
                )
                logger.debug(
                    f"Activity Feed({self.request.user} updated Salary Percentage Adjustment({previous_salary_adjustment_percentage.percentage_adjustment}): Percentage Adjustment: {previous_salary_adjustment_percentage.percentage_adjustment}% → {salary_adjustment_percentage_update.percentage_adjustment}%) created."
                )


class ListSalaryAdjustmentPercentageAPIView(generics.ListAPIView):
    queryset = SalaryAdjustmentPercentage.objects.all()
    serializer_class = serializers.SalaryAdjustmentPercentageSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class RetrieveSalaryAdjustmentPercentageAPIView(generics.RetrieveAPIView):
    queryset = SalaryAdjustmentPercentage.objects.all()
    serializer_class = serializers.SalaryAdjustmentPercentageSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class DeleteSalaryAdjustmentPercentageAPIView(generics.DestroyAPIView):
    queryset = SalaryAdjustmentPercentage.objects.all()
    serializer_class = serializers.SalaryAdjustmentPercentageSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.delete()
            logger.debug(f"Salary Adjustment Percentage({instance}) deleted.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"The Salary Adjustment Percentage({instance.percentage_adjustment}%) was deleted by {self.request.user}",
            )
            logger.debug(
                f"Activity feed(The Salary Adjustment Percentage({instance.percentage_adjustment}%) was deleted by {self.request.user}) created."
            )


# *INCOMPLETE OCCURRENCE
class CreateIncompleteOccurrenceAPIView(generics.CreateAPIView):
    queryset = IncompleteOccurrence.objects.all()
    serializer_class = serializers.IncompleteOccurrenceWriteSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.IncompleteOccurrenceReadSerializer(
            self.incomplete_occurrence
        )

        return Response(read_serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        with transaction.atomic():
            self.incomplete_occurrence = serializer.save(
                created_by=self.request.user, updated_by=self.request.user
            )
            logger.debug(
                f"Incomplete Occurrence({self.incomplete_occurrence}) created."
            )

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=(
                    f"{self.request.user} added a new Incomplete Occurrence(ID: {self.incomplete_occurrence.id} — Authority: {self.incomplete_occurrence.authority} — Event: {self.incomplete_occurrence.event})"
                ),
            )
            logger.debug(
                f"Activity Feed({self.request.user} added a new Incomplete Occurrence(ID: {self.incomplete_occurrence.id} — Authority: {self.incomplete_occurrence.authority} — Event: {self.incomplete_occurrence.event}) created."
            )

            # Flag created record
            create_flag(self.incomplete_occurrence, self.request.user)


class EditIncompleteOccurrenceAPIView(generics.UpdateAPIView):
    queryset = IncompleteOccurrence.objects.all()
    serializer_class = serializers.IncompleteOccurrenceUpdateSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.IncompleteOccurrenceReadSerializer(
            self.incomplete_occurrence_update
        )

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        with transaction.atomic():
            previous_incomplete_occurrence = self.get_object()
            self.incomplete_occurrence_update = serializer.save(
                updated_by=self.request.user
            )
            logger.debug(
                f"Incomplete Occurrence({previous_incomplete_occurrence}) updated."
            )

            changes = incomplete_occurrence_changes(
                previous_incomplete_occurrence, self.incomplete_occurrence_update
            )
            print("changes -> ", changes)

            if changes:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=f"{self.request.user} updated Incomplete Occurrence(ID: {previous_incomplete_occurrence.id} — Authority: {previous_incomplete_occurrence.authority} — Event: {previous_incomplete_occurrence.event}): {changes}",
                )
                logger.debug(
                    f"Activity feed({self.request.user} updated Incomplete Occurrence(ID: {previous_incomplete_occurrence.id} — Authority: {previous_incomplete_occurrence.authority} — Event: {previous_incomplete_occurrence.event}): {changes})) created."
                )


class RetrieveIncompleteOccurrenceAPIView(generics.RetrieveAPIView):
    queryset = IncompleteOccurrence.objects.select_related(
        "created_by", "updated_by", "grade", "level_step", "event"
    )
    lookup_field = "pk"
    serializer_class = serializers.IncompleteOccurrenceReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class ListEmployeeIncompleteOccurrenceAPIView(generics.ListAPIView):
    serializer_class = serializers.IncompleteOccurrenceReadSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        incomplete_occurrence = employee.incomplete_occurrence.select_related(
            "created_by", "updated_by", "grade", "level_step", "event"
        )
        return incomplete_occurrence


class ListIncompleteOccurrenceAPIView(generics.ListAPIView):
    queryset = IncompleteOccurrence.objects.select_related(
        "created_by", "updated_by", "grade", "level_step", "event"
    )
    serializer_class = serializers.IncompleteOccurrenceReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class DeleteIncompleteOccurrenceAPIView(generics.DestroyAPIView):
    queryset = IncompleteOccurrence.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.IncompleteOccurrenceWriteSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        with transaction.atomic():
            incomplete_occurrence_id = instance.id
            instance.delete()
            logger.debug(f"Incomplete Occurrence({instance}) deleted.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"The Incomplete Occurrence(ID: {incomplete_occurrence_id} — Authority: {instance.authority} — Event: {instance.event}) was deleted by {self.request.user}",
            )
            logger.debug(
                f"Activity feed(The Incomplete Occurrence(ID: {incomplete_occurrence_id} — Authority: {instance.authority} — Event: {instance.event})) created."
            )

            # Delete associated flags
            delete_flag(instance, incomplete_occurrence_id, self.request.user)
