from rest_framework import generics
import logging
from . import serializers
from .models import PreviousGovernmentService
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from .utils import previous_government_service_changes

logger = logging.getLogger(__name__)


class CreatePreviousGovernmentServiceAPIView(generics.CreateAPIView):
    serializer_class = serializers.PreviousGovernmentServiceWriteSerializer
    queryset = PreviousGovernmentService.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.PreviousGovernmentServiceReadSerializer(
            self.government_service
        )

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.government_service = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Previous Government Service({self.government_service}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Previous Government Service(Institution: {self.government_service.institution} — Position: {self.government_service.position})",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Previous Government Service(Institution: {self.government_service.institution} — Position: {self.government_service.position})) created."
        )


class EditPreviousGovernmentServiceAPIView(generics.UpdateAPIView):
    queryset = PreviousGovernmentService.objects.all()
    serializer_class = serializers.PreviousGovernmentServiceWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.PreviousGovernmentServiceReadSerializer(
            self.government_service_update
        )

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_government_service = self.get_object()
        self.government_service_update = serializer.save(updated_by=self.request.user)
        logger.debug(
            f"Previous Government Service({previous_government_service}) updated."
        )

        changes = previous_government_service_changes(
            previous_government_service, self.government_service_update
        )

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Previous Government Service(Institution: {previous_government_service.institution} — Position: {previous_government_service.position}): {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Previous Government Service(Institution: {previous_government_service.institution} — Position: {previous_government_service.position}): {changes}) created."
            )


class ListEmployeePreviousGovernmentServiceAPIView(generics.ListAPIView):
    serializer_class = serializers.PreviousGovernmentServiceReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        previous_government_service = (
            employee.previous_government_service.select_related(
                "created_by", "updated_by"
            )
        )
        return previous_government_service


class RetrievePreviousGovernmentServiceAPIView(generics.RetrieveAPIView):
    queryset = PreviousGovernmentService.objects.all()
    serializer_class = serializers.PreviousGovernmentServiceReadSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeletePreviousGovernmentServiceAPIView(generics.DestroyAPIView):
    queryset = PreviousGovernmentService.objects.all()
    serializer_class = serializers.PreviousGovernmentServiceWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Previous Government Service({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Previous Government Service(Institution: {instance.institution} — Position: {instance.position}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Previous Government Service(Institution: {instance.institution} — Position: {instance.position}) was deleted by {self.request.user}) created."
        )
