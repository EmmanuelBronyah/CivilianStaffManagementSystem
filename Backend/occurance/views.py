from rest_framework import generics
from .models import Occurrence
from .serializer import OccurrenceSerializer
from rest_framework.permissions import IsAuthenticated
from employees.permissions import IsAdminUserOrStandardUser
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
from activity_feeds.models import ActivityFeeds
import logging
from .utils import occurrence_changes
from employees.models import Employee
from django.shortcuts import get_object_or_404


logger = logging.getLogger(__name__)


class CreateOccurrenceAPIView(generics.CreateAPIView):
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer
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
    serializer_class = OccurrenceSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_update(self, serializer):
        previous_occurrence = self.get_object()
        occurrence_update = serializer.save(updated_by=self.request.user)
        logger.debug(f"Occurrence({previous_occurrence}) updated.")

        changes = occurrence_changes(previous_occurrence, occurrence_update)

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated occurrence '{previous_occurrence.employee.service_id} — {previous_occurrence.authority} — {previous_occurrence.event}': {changes}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated occurrence '{previous_occurrence.employee.service_id} — {previous_occurrence.authority} — {previous_occurrence.event}': {changes}) created."
        )


class RetrieveEmployeeOccurrenceAPIView(generics.ListAPIView):
    serializer_class = OccurrenceSerializer
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
    serializer_class = OccurrenceSerializer
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
