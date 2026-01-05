from rest_framework import generics
import logging
from . import serializers
from .models import Identity
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from .utils import identity_record_changes

logger = logging.getLogger(__name__)


class CreateIdentityAPIView(generics.CreateAPIView):
    serializer_class = serializers.IdentitySerializer
    queryset = Identity.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_create(self, serializer):
        identity = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Identity for Employee({identity.employee.service_id}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Identity for Employee: '{identity.employee.service_id}'",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Identity for Employee: '{identity.employee.service_id}') created."
        )


class EditIdentityAPIView(generics.UpdateAPIView):
    queryset = Identity.objects.all()
    serializer_class = serializers.IdentitySerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_update(self, serializer):
        previous_identity = self.get_object()
        identity_update = serializer.save()
        logger.debug(
            f"Identity for Employee({previous_identity.employee.service_id}) updated."
        )

        changes = identity_record_changes(previous_identity, identity_update)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Identity for Employee '{previous_identity.employee.service_id}': {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Identity for Employee '{previous_identity.employee.service_id}': {changes}) created."
            )


class ListEmployeeIdentityAPIView(generics.ListAPIView):
    queryset = Identity.objects.all()
    serializer_class = serializers.IdentitySerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        identity = employee.identities.all()
        return identity


class RetrieveIdentityAPIView(generics.RetrieveAPIView):
    queryset = Identity.objects.all()
    serializer_class = serializers.IdentitySerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteIdentityAPIView(generics.DestroyAPIView):
    queryset = Identity.objects.all()
    serializer_class = serializers.IdentitySerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Identity for Employee({instance.employee.service_id}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Identity for Employee '{instance.employee.service_id}' was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Identity for Employee '{instance.employee.service_id}' was deleted by {self.request.user}) created."
        )
