from rest_framework import generics
import logging
from . import serializers
from .models import Spouse
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from .utils import spouse_record_changes

logger = logging.getLogger(__name__)

# TODO: Sort Occurrences based on CEM number


class CreateSpouseAPIView(generics.CreateAPIView):
    serializer_class = serializers.SpouseWriteSerializer
    queryset = Spouse.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.SpouseReadSerializer(self.spouse)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.spouse = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Spouse({self.spouse.spouse_name}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Spouse({self.spouse.spouse_name})",
        )

        logger.debug(
            f"Activity Feed({self.request.user} added a new Spouse({self.spouse.spouse_name})) created."
        )


class EditSpouseAPIView(generics.UpdateAPIView):
    queryset = Spouse.objects.all()
    serializer_class = serializers.SpouseWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.SpouseReadSerializer(self.spouse_update)

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_spouse = self.get_object()
        self.spouse_update = serializer.save(updated_by=self.request.user)
        logger.debug(f"Spouse({previous_spouse.spouse_name}) updated.")

        changes = spouse_record_changes(previous_spouse, self.spouse_update)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Spouse({previous_spouse.spouse_name}): {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Spouse({previous_spouse.spouse_name}): {changes}) created."
            )


class ListEmployeeSpouseAPIView(generics.ListAPIView):
    serializer_class = serializers.SpouseReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        spouse = employee.spouse.select_related("created_by", "updated_by")
        return spouse


class RetrieveSpouseAPIView(generics.RetrieveAPIView):
    queryset = Spouse.objects.select_related("created_by", "updated_by")
    serializer_class = serializers.SpouseReadSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteSpouseAPIView(generics.DestroyAPIView):
    queryset = Spouse.objects.all()
    serializer_class = serializers.SpouseWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Spouse({instance.spouse_name}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Spouse({instance.spouse_name}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Spouse({instance.spouse_name}) was deleted by {self.request.user}) created."
        )
