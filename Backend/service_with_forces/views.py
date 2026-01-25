from rest_framework import generics
import logging
from . import serializers
from .models import ServiceWithForces, MilitaryRanks, IncompleteServiceWithForcesRecords
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from .utils import (
    military_rank_changes,
    service_with_forces_changes,
    incomplete_service_with_forces_changes,
)
from flags.services import create_flag, delete_flag
from employees.views import LargeResultsSetPagination
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

# TODO: Ensure all perform update functions include the updated by key


# * SERVICE WITH FORCES
class CreateServiceWithForcesAPIView(generics.CreateAPIView):
    serializer_class = serializers.ServiceWithForcesWriteSerializer
    queryset = ServiceWithForces.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.ServiceWithForcesReadSerializer(
            self.service_with_forces
        )

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.service_with_forces = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Service With Forces({self.service_with_forces}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Service With Forces(Service Date: {self.service_with_forces.service_date} — Last Unit: {self.service_with_forces.last_unit})",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Service With Forces(Service Date: {self.service_with_forces.service_date} — Last Unit: {self.service_with_forces.last_unit})) created."
        )


class EditServiceWithForcesAPIView(generics.UpdateAPIView):
    queryset = ServiceWithForces.objects.all()
    serializer_class = serializers.ServiceWithForcesWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.ServiceWithForcesReadSerializer(
            self.service_with_forces_update
        )

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        pervious_service_with_forces = self.get_object()
        self.service_with_forces_update = serializer.save(updated_by=self.request.user)
        logger.debug(f"Service With Forces({pervious_service_with_forces}) updated.")

        changes = service_with_forces_changes(
            pervious_service_with_forces, self.service_with_forces_update
        )

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Service With Forces(Service Date: {pervious_service_with_forces.service_date} — Last Unit: {pervious_service_with_forces.last_unit}): {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Service With Forces(Service Date: {pervious_service_with_forces.service_date} — Last Unit: {pervious_service_with_forces.last_unit}): {changes}) created."
            )


class ListEmployeeServiceWithForcesAPIView(generics.ListAPIView):
    serializer_class = serializers.ServiceWithForcesReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        service_with_forces = employee.service_with_forces.select_related(
            "created_by", "updated_by", "military_rank", "last_unit"
        )
        return service_with_forces


class RetrieveServiceWithForcesAPIView(generics.RetrieveAPIView):
    queryset = ServiceWithForces.objects.select_related(
        "created_by", "updated_by", "military_rank", "last_unit"
    )
    serializer_class = serializers.ServiceWithForcesReadSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteServiceWithForcesAPIView(generics.DestroyAPIView):
    queryset = ServiceWithForces.objects.all()
    serializer_class = serializers.ServiceWithForcesWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Service With Forces({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Service With Forces(Service Date: {instance.service_date} — Last Unit: {instance.last_unit}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Service With Forces(Service Date: {instance.service_date} — Last Unit: {instance.last_unit}) was deleted by {self.request.user}) created."
        )


# * MILITARY RANKS
class CreateMilitaryRanksAPIView(generics.CreateAPIView):
    serializer_class = serializers.MilitaryRanksSerializer
    queryset = MilitaryRanks.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        military_rank = serializer.save()
        logger.debug(f"Military Rank({military_rank}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Military Rank({military_rank.rank})",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Military Rank({military_rank.rank})) created."
        )


class EditMilitaryRanksAPIView(generics.UpdateAPIView):
    queryset = MilitaryRanks.objects.all()
    serializer_class = serializers.MilitaryRanksSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        previous_military_rank = self.get_object()
        military_rank_update = serializer.save()
        logger.debug(f"Military Rank({previous_military_rank}) updated.")

        changes = military_rank_changes(previous_military_rank, military_rank_update)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Military Rank({previous_military_rank.rank}): {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Military Rank({previous_military_rank.rank}): {changes}) created."
            )


class ListMilitaryRanksAPIView(generics.ListAPIView):
    queryset = MilitaryRanks.objects.all()
    serializer_class = serializers.MilitaryRanksSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class RetrieveMilitaryRanksAPIView(generics.RetrieveAPIView):
    queryset = MilitaryRanks.objects.all()
    serializer_class = serializers.MilitaryRanksSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteMilitaryRanksAPIView(generics.DestroyAPIView):
    queryset = MilitaryRanks.objects.all()
    serializer_class = serializers.MilitaryRanksSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Military Rank({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Military Rank({instance.rank}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Military Rank({instance.rank}) was deleted by {self.request.user}) created."
        )


# INCOMPLETE SERVICE WITH FORCES
class CreateIncompleteServiceWithForcesRecordsAPIView(generics.CreateAPIView):
    queryset = IncompleteServiceWithForcesRecords.objects.all()
    serializer_class = serializers.IncompleteServiceWithForcesRecordsWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        read_serializer = serializers.IncompleteServiceWithForcesReadSerializer(
            self.service_with_forces
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.service_with_forces = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(
            f"Incomplete Service With Forces({self.service_with_forces}) created."
        )

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Incomplete Service With Forces(ID: {self.service_with_forces.id})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Incomplete Service With Forces(ID: {self.service_with_forces.id})) created."
        )

        # Flag created record
        create_flag(self.service_with_forces, self.request.user)


class RetrieveIncompleteServiceWithForcesRecordsAPIView(generics.RetrieveAPIView):
    queryset = IncompleteServiceWithForcesRecords.objects.select_related(
        "created_by", "updated_by", "last_unit", "military_rank"
    )
    lookup_field = "pk"
    serializer_class = serializers.IncompleteServiceWithForcesReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class ListIncompleteServiceWithForcesRecordsAPIView(generics.ListAPIView):
    queryset = IncompleteServiceWithForcesRecords.objects.select_related(
        "created_by", "updated_by", "last_unit", "military_rank"
    )
    serializer_class = serializers.IncompleteServiceWithForcesReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class ListEmployeeIncompleteServiceWithForcesRecordsAPIView(generics.ListAPIView):
    serializer_class = serializers.IncompleteServiceWithForcesReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        incomplete_service_with_forces_records = (
            employee.incomplete_service_with_forces_records.select_related(
                "created_by", "updated_by", "last_unit", "military_rank"
            )
        )
        return incomplete_service_with_forces_records


class EditIncompleteServiceWithForcesRecordsAPIView(generics.UpdateAPIView):
    queryset = IncompleteServiceWithForcesRecords.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.IncompleteServiceWithForcesRecordsWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = serializers.IncompleteServiceWithForcesReadSerializer(
            self.service_with_forces
        )
        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_service_with_forces = self.get_object()
        self.service_with_forces = serializer.save(updated_by=self.request.user)
        logger.debug(
            f"Incomplete Service With Forces({previous_service_with_forces}) updated."
        )

        changes = incomplete_service_with_forces_changes(
            previous_service_with_forces, self.service_with_forces
        )

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Incomplete Service With Forces(ID: {self.service_with_forces.id}): {changes}",
            )
            logger.debug(
                f"Activity feed({self.request.user} updated Incomplete Service With Forces(ID: {self.service_with_forces.id}): {changes}) created."
            )


class DeleteIncompleteServiceWithForcesRecordsAPIView(generics.DestroyAPIView):
    queryset = IncompleteServiceWithForcesRecords.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.IncompleteServiceWithForcesRecordsWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        service_with_forces_id = instance.id
        instance.delete()
        logger.debug(f"Incomplete Service With Forces({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Incomplete Service With Forces(ID: {service_with_forces_id}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Incomplete Service With Forces(ID: {service_with_forces_id}) was deleted by {self.request.user}) created."
        )

        # Delete associated flags
        delete_flag(instance, service_with_forces_id, self.request.user)
