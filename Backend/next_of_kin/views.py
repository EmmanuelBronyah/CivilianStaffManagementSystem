from rest_framework import generics
import logging
from . import serializers
from .models import EmergencyOrNextOfKin
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from .utils import next_of_kin_record_changes
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


class CreateNextOfKinAPIView(generics.CreateAPIView):
    serializer_class = serializers.EmergencyOrNextOfKinWriteSerializer
    queryset = EmergencyOrNextOfKin.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.EmergencyOrNextOfKinReadSerializer(
            self.next_of_kin
        )

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.next_of_kin = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Next Of Kin({self.next_of_kin}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Next Of Kin(Name: {self.next_of_kin.name} — Relation: {self.next_of_kin.relation})",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Next Of Kin(Name: {self.next_of_kin.name} — Relation: {self.next_of_kin.relation})) created."
        )


class EditNextOfKinAPIView(generics.UpdateAPIView):
    queryset = EmergencyOrNextOfKin.objects.all()
    serializer_class = serializers.EmergencyOrNextOfKinWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.EmergencyOrNextOfKinReadSerializer(
            self.next_of_kin_update
        )

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_next_of_kin = self.get_object()
        self.next_of_kin_update = serializer.save(updated_by=self.request.user)
        logger.debug(f"Next Of Kin({previous_next_of_kin}) updated.")

        changes = next_of_kin_record_changes(
            previous_next_of_kin, self.next_of_kin_update
        )

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Next Of Kin(Name: {previous_next_of_kin.name} — Relation: {previous_next_of_kin.relation}): {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Next Of Kin(Name: {previous_next_of_kin.name} — Relation: {previous_next_of_kin.relation}): {changes}) created."
            )


class ListEmployeeNextOfKinAPIView(generics.ListAPIView):
    queryset = EmergencyOrNextOfKin.objects.select_related("created_by", "updated_by")
    serializer_class = serializers.EmergencyOrNextOfKinReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        next_of_kin = employee.next_of_kin.all()
        return next_of_kin


class RetrieveNextOfKinAPIView(generics.RetrieveAPIView):
    queryset = EmergencyOrNextOfKin.objects.select_related("created_by", "updated_by")
    serializer_class = serializers.EmergencyOrNextOfKinReadSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteNextOfKinAPIView(generics.DestroyAPIView):
    queryset = EmergencyOrNextOfKin.objects.all()
    serializer_class = serializers.EmergencyOrNextOfKinWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Next Of Kin({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Next Of Kin(Name: {instance.name} — Relation: {instance.relation}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Next Of Kin(Name: {instance.name} — Relation: {instance.relation}) was deleted by {self.request.user}) created."
        )
