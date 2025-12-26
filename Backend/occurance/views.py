from rest_framework import generics
from .models import Occurrence, LevelStep, SalaryPercentageAdjustment
from . import serializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from employees.permissions import IsAdminUserOrStandardUser
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
from activity_feeds.models import ActivityFeeds
import logging
from .utils import occurrence_changes, level_step_changes
from employees.models import Employee
from django.shortcuts import get_object_or_404

# TODO: Salaries should be greater than 0 or a reasonably specified amount

logger = logging.getLogger(__name__)


# * OCCURRENCE
class CreateOccurrenceAPIView(generics.CreateAPIView):
    queryset = Occurrence.objects.all()
    serializer_class = serializer.OccurrenceSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        occurrence_data = request.data
        is_many = isinstance(occurrence_data, list)

        serializer = self.get_serializer(data=occurrence_data, many=is_many)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        occurrence = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        records = (
            ", ".join([str(record) for record in occurrence])
            if isinstance(occurrence, list)
            else occurrence
        )
        logger.debug(f"Occurrence({records}) created.")

        if isinstance(occurrence, list):
            for record in occurrence:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=(
                        f"{self.request.user} added a new occurrence: '{record.employee.service_id} — {record.authority} — {record.event}'"
                    ),
                )
        else:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=(
                    f"{self.request.user} added a new occurrence: '{occurrence.employee.service_id} — {occurrence.authority} — {occurrence.event}'"
                ),
            )


class EditOccurrenceAPIView(generics.UpdateAPIView):
    queryset = Occurrence.objects.all()
    serializer_class = serializer.OccurrenceSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_occurrence = self.get_object()
        occurrence_update = serializer.save(updated_by=self.request.user)
        logger.debug(f"Occurrence({previous_occurrence}) updated.")

        changes = occurrence_changes(previous_occurrence, occurrence_update)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated occurrence '{previous_occurrence.employee.service_id} — {previous_occurrence.authority} — {previous_occurrence.event}': {changes}",
            )
            logger.debug(
                f"Activity feed({self.request.user} updated occurrence '{previous_occurrence.employee.service_id} — {previous_occurrence.authority} — {previous_occurrence.event}': {changes}) created."
            )


class RetrieveEmployeeOccurrenceAPIView(generics.ListAPIView):
    serializer_class = serializer.OccurrenceSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        occurrences = employee.occurrences.all()
        return occurrences


class DeleteOccurrenceAPIView(generics.DestroyAPIView):
    queryset = Occurrence.objects.all()
    lookup_field = "pk"
    serializer_class = serializer.OccurrenceSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Occurrence({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The occurrence '{instance.employee.service_id} — {instance.authority} — {instance.event}' was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The occurrence '{instance.employee.service_id} — {instance.authority} — {instance.event}' was deleted by {self.request.user}) created."
        )


# * LEVEL|STEP
class CreateLevelStepAPIView(generics.CreateAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializer.LevelStepSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        level_step = serializer.save()
        logger.debug(f"Level|Step({level_step}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=(
                f"{self.request.user} added a new Level|Step: '{level_step.level_step} — {level_step.monthly_salary}'"
            ),
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Level|Step: '{level_step.level_step} — {level_step.monthly_salary}') created."
        )


class EditLevelStepAPIView(generics.UpdateAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializer.LevelStepSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_level_step = self.get_object()
        level_step_update = serializer.save()
        logger.debug(f"Level|Step({previous_level_step}) updated.")

        changes = level_step_changes(previous_level_step, level_step_update)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Level|Step '{previous_level_step.level_step} — {previous_level_step.monthly_salary}': {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Level|Step '{previous_level_step.level_step} — {previous_level_step.monthly_salary}': {changes}) created."
            )


class ListLevelStepAPIView(generics.ListAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializer.LevelStepSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class RetrieveLevelStepAPIView(generics.RetrieveAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializer.LevelStepSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class DeleteLevelStepAPIView(generics.DestroyAPIView):
    queryset = LevelStep.objects.all()
    serializer_class = serializer.LevelStepSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Level|Step({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Level|Step '{instance.level_step} — {instance.monthly_salary}' was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Level|Step '{instance.level_step} — {instance.monthly_salary}' was deleted by {self.request.user}) created."
        )
