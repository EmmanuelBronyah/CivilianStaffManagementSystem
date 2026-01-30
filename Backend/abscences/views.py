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
from django.db import transaction

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

        read_serializer = serializers.AbsencesReadSerializer(
            self.absences, many=is_many
        )

        return Response(read_serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        with transaction.atomic():
            self.absences = serializer.save(
                created_by=self.request.user, updated_by=self.request.user
            )
            records = (
                ", ".join([str(record) for record in self.absences])
                if isinstance(self.absences, list)
                else self.absences
            )
            logger.debug(f"Absences({records}) created.")

            if isinstance(self.absences, list):
                for record in self.absences:
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
                    activity=f"{self.request.user} added a new Absences({self.absences.absence})",
                )
                logger.debug(
                    f"Activity Feed({self.request.user} added a new Absences({self.absences.absence})) created."
                )


class EditAbsencesAPIView(generics.UpdateAPIView):
    queryset = Absences.objects.all()
    serializer_class = serializers.AbsencesWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.AbsencesReadSerializer(self.absences_update)

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        with transaction.atomic():
            previous_absences = self.get_object()
            self.absences_update = serializer.save(updated_by=self.request.user)
            logger.debug(f"Absences({previous_absences}) updated.")

            changes = absences_changes(previous_absences, self.absences_update)

            if changes:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=f"{self.request.user} updated Absences({previous_absences.absence}): {changes}",
                )
                logger.debug(
                    f"Activity Feed({self.request.user} updated Absences({previous_absences.absence}): {changes}) created."
                )


class ListEmployeeAbsencesAPIView(generics.ListAPIView):
    serializer_class = serializers.AbsencesReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        absences = employee.absences.select_related("created_by", "updated_by")
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
        with transaction.atomic():
            instance.delete()
            logger.debug(f"Absences({instance}) deleted.")

            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"The Absences({instance.absence}) was deleted by {self.request.user}",
            )
            logger.debug(
                f"Activity feed(The Absences({instance.absence}) was deleted by {self.request.user}) created."
            )
