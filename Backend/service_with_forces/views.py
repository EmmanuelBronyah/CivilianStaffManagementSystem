from rest_framework import generics
import logging
from . import serializers
from .models import ServiceWithForces, MilitaryRanks
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from .utils import military_rank_changes, service_with_forces_changes

logger = logging.getLogger(__name__)

# TODO: Ensure all perform update functions include the updated by key


# * SERVICE WITH FORCES
class CreateServiceWithForcesAPIView(generics.CreateAPIView):
    serializer_class = serializers.ServiceWithForcesSerializer
    queryset = ServiceWithForces.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_create(self, serializer):
        service_with_forces = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Service With Forces({service_with_forces}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Service With Forces: '{service_with_forces.service_date} — {service_with_forces.last_unit}'",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Service With Forces: '{service_with_forces.service_date} — {service_with_forces.last_unit}') created."
        )


class EditServiceWithForcesAPIView(generics.UpdateAPIView):
    queryset = ServiceWithForces.objects.all()
    serializer_class = serializers.ServiceWithForcesSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_update(self, serializer):
        pervious_service_with_forces = self.get_object()
        service_with_forces_update = serializer.save()
        logger.debug(f"Service With Forces({pervious_service_with_forces}) updated.")

        changes = service_with_forces_changes(
            pervious_service_with_forces, service_with_forces_update
        )

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Service With Forces '{pervious_service_with_forces.service_date} — {pervious_service_with_forces.last_unit}': {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Service With Forces '{pervious_service_with_forces.service_date} — {pervious_service_with_forces.last_unit}': {changes}) created."
            )


class ListEmployeeServiceWithForcesAPIView(generics.ListAPIView):
    queryset = ServiceWithForces.objects.all()
    serializer_class = serializers.ServiceWithForcesSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        service_with_forces = employee.service_with_forces.all()
        return service_with_forces


class RetrieveServiceWithForcesAPIView(generics.RetrieveAPIView):
    queryset = ServiceWithForces.objects.all()
    serializer_class = serializers.ServiceWithForcesSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteServiceWithForcesAPIView(generics.DestroyAPIView):
    queryset = ServiceWithForces.objects.all()
    serializer_class = serializers.ServiceWithForcesSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Service With Forces({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Service With Forces '{instance.service_date} — {instance.last_unit}' was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Service With Forces '{instance.service_date} — {instance.last_unit}' was deleted by {self.request.user}) created."
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
            activity=f"{self.request.user} added a new Military Rank: '{military_rank.rank}'",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Military Rank: '{military_rank.rank}') created."
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
                activity=f"{self.request.user} updated Military Rank '{previous_military_rank.rank}': {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Military Rank '{previous_military_rank.rank}': {changes}) created."
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
            activity=f"The Military Rank '{instance.rank}' was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Military Rank '{instance.rank}' was deleted by {self.request.user}) created."
        )
