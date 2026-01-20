from rest_framework import generics
import logging
from . import serializers
from .models import Children
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from .utils import child_record_changes

logger = logging.getLogger(__name__)


class CreateChildRecordAPIView(generics.CreateAPIView):
    serializer_class = serializers.ChildrenWriteSerializer
    queryset = Children.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_create(self, serializer):
        child_record = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Child Record({child_record}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Child Record(Child Name: {child_record.child_name} — Date of Birth: {child_record.dob})",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Child Record(Child Name: {child_record.child_name} — Date of Birth: {child_record.dob})) created."
        )


class EditChildRecordAPIView(generics.UpdateAPIView):
    queryset = Children.objects.all()
    serializer_class = serializers.ChildrenWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_update(self, serializer):
        previous_child_record = self.get_object()
        child_record_update = serializer.save()
        logger.debug(f"Child Record({previous_child_record}) updated.")

        changes = child_record_changes(previous_child_record, child_record_update)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Child Record(Child Name: {previous_child_record.child_name} — Date of Birth: {previous_child_record.dob}): {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Child Record(Child Name: {previous_child_record.child_name} — Date of Birth: {previous_child_record.dob}): {changes}) created."
            )


class ListEmployeeChildrenAPIView(generics.ListAPIView):
    queryset = Children.objects.select_related("created_by", "updated_by", "gender")
    serializer_class = serializers.ChildrenReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        children = employee.children.all()
        return children


class RetrieveChildRecordAPIView(generics.RetrieveAPIView):
    queryset = Children.objects.select_related("created_by", "updated_by", "gender")
    serializer_class = serializers.ChildrenReadSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteChildRecordAPIView(generics.DestroyAPIView):
    queryset = Children.objects.all()
    serializer_class = serializers.ChildrenWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Child Record({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Child Record(Child Name: {instance.child_name} — Date of Birth: {instance.dob}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Child Record(Child Name: {instance.child_name} — Date of Birth: {instance.dob}) was deleted by {self.request.user}) created."
        )
