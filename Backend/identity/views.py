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
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


class CreateIdentityAPIView(generics.CreateAPIView):
    serializer_class = serializers.IdentityWriteSerializer
    queryset = Identity.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.IdentityReadSerializer(self.identity)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.identity = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(
            f"Identity for Employee({self.identity.employee.service_id}) created."
        )

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Identity(Service ID: {self.identity.employee.service_id})",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Identity(Service ID: {self.identity.employee.service_id})) created."
        )


class EditIdentityAPIView(generics.UpdateAPIView):
    queryset = Identity.objects.all()
    serializer_class = serializers.IdentityWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.IdentityReadSerializer(self.identity_update)

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_identity = self.get_object()
        self.identity_update = serializer.save(updated_by=self.request.user)
        logger.debug(
            f"Identity for Employee({previous_identity.employee.service_id}) updated."
        )

        changes = identity_record_changes(previous_identity, self.identity_update)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Identity(Service ID: {previous_identity.employee.service_id}): {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Identity(Service ID: {previous_identity.employee.service_id}): {changes}) created."
            )


class RetrieveEmployeeIdentityAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.IdentityReadSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_object(self):
        service_id = self.kwargs.get("pk")
        return get_object_or_404(
            Identity.objects.select_related("created_by", "updated_by"),
            employee__pk=service_id,
        )


class DeleteIdentityAPIView(generics.DestroyAPIView):
    queryset = Identity.objects.all()
    serializer_class = serializers.IdentityWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Identity for Employee({instance.employee.service_id}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Identity(Service ID: {instance.employee.service_id}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Identity(Service ID: {instance.employee.service_id}) was deleted by {self.request.user}) created."
        )
