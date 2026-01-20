from rest_framework import generics
import logging
from . import serializers
from .models import Absences
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from .utils import absences_changes
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


class CreateAbsencesAPIView(generics.CreateAPIView):
    serializer_class = serializers.AbsencesWriteSerializer
    queryset = Absences.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def create(self, request, *args, **kwargs):
        absences_data = request.data
        is_many = isinstance(absences_data, list)

        serializer = self.get_serializer(data=absences_data, many=is_many)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        absences = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        records = (
            ", ".join([str(record) for record in absences])
            if isinstance(absences, list)
            else absences
        )
        logger.debug(f"Absences({records}) created.")

        if isinstance(absences, list):
            for record in absences:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=f"{self.request.user} added a new Absences({record.absence})",
                )
                logger.debug(
                    f"Activity Feed({self.request.user} added a new Absences({record.absence})) created."
                )
        else:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} added a new Absences({absences.absence})",
            )
            logger.debug(
                f"Activity Feed({self.request.user} added a new Absences({absences.absence})) created."
            )


class EditAbsencesAPIView(generics.UpdateAPIView):
    queryset = Absences.objects.all()
    serializer_class = serializers.AbsencesWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_update(self, serializer):
        previous_absences = self.get_object()
        absences_update = serializer.save(updated_by=self.request.user)
        logger.debug(f"Absences({previous_absences}) updated.")

        changes = absences_changes(previous_absences, absences_update)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Absences({previous_absences.absence}): {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Absences({previous_absences.absence}): {changes}) created."
            )


class ListEmployeeAbsencesAPIView(generics.ListAPIView):
    queryset = Absences.objects.select_related("created_by", "updated_by")
    serializer_class = serializers.AbsencesReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        absences = employee.absences.all()
        return absences


class RetrieveAbsencesAPIView(generics.RetrieveAPIView):
    queryset = Absences.objects.select_related("created_by", "updated_by")
    serializer_class = serializers.AbsencesReadSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteAbsencesAPIView(generics.DestroyAPIView):
    queryset = Absences.objects.all()
    serializer_class = serializers.AbsencesWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Absences({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Absences({instance.absence}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Absences({instance.absence}) was deleted by {self.request.user}) created."
        )
