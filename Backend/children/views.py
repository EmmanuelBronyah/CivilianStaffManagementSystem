from rest_framework import generics
import logging
from . import serializers
from .models import Children, InCompleteChildRecords
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from .utils import child_record_changes, incomplete_child_record_changes
from flags.services import create_flag, delete_flag
from employees.views import LargeResultsSetPagination
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


# todo: implement search
# todo: service id lesser than 5
class CreateChildRecordAPIView(generics.CreateAPIView):
    serializer_class = serializers.ChildrenWriteSerializer
    queryset = Children.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.ChildrenReadSerializer(self.child_record)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.child_record = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Child Record({self.child_record}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Child Record(Child Name: {self.child_record.child_name} — Date of Birth: {self.child_record.dob})",
        )
        logger.debug(
            f"Activity Feed({self.request.user} added a new Child Record(Child Name: {self.child_record.child_name} — Date of Birth: {self.child_record.dob})) created."
        )


class EditChildRecordAPIView(generics.UpdateAPIView):
    queryset = Children.objects.all()
    serializer_class = serializers.ChildrenWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.ChildrenReadSerializer(self.child_record_update)

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_child_record = self.get_object()
        self.child_record_update = serializer.save()
        logger.debug(f"Child Record({previous_child_record}) updated.")

        changes = child_record_changes(previous_child_record, self.child_record_update)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Child Record(Child Name: {previous_child_record.child_name} — Date of Birth: {previous_child_record.dob}): {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Child Record(Child Name: {previous_child_record.child_name} — Date of Birth: {previous_child_record.dob}): {changes}) created."
            )


class ListEmployeeChildrenAPIView(generics.ListAPIView):
    serializer_class = serializers.ChildrenReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        children = employee.children.select_related(
            "created_by", "updated_by", "gender"
        )
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


# * INCOMPLETE CHILD RECORD
class CreateInCompleteChildRecordsAPIView(generics.CreateAPIView):
    queryset = InCompleteChildRecords.objects.all()
    serializer_class = serializers.InCompleteChildRecordsWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        read_serializer = serializers.InCompleteChildRecordsReadSerializer(
            self.child_record
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.child_record = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Incomplete Child Record({self.child_record}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Incomplete Child Record(ID: {self.child_record.id})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Incomplete Child Record(ID: {self.child_record.id})) created."
        )

        # Flag created record
        create_flag(self.child_record, self.request.user)


class RetrieveInCompleteChildRecordsAPIView(generics.RetrieveAPIView):
    queryset = InCompleteChildRecords.objects.select_related(
        "gender", "created_by", "updated_by"
    )
    lookup_field = "pk"
    serializer_class = serializers.InCompleteChildRecordsReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class ListInCompleteChildRecordsAPIView(generics.ListAPIView):
    queryset = InCompleteChildRecords.objects.select_related(
        "gender", "created_by", "updated_by"
    )
    serializer_class = serializers.InCompleteChildRecordsReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class ListEmployeeInCompleteChildRecordsAPIView(generics.ListAPIView):
    serializer_class = serializers.InCompleteChildRecordsReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        incomplete_child_records = employee.incomplete_child_records.select_related(
            "gender", "created_by", "updated_by"
        )
        return incomplete_child_records


class EditInCompleteChildRecordsAPIView(generics.UpdateAPIView):
    queryset = InCompleteChildRecords.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.InCompleteChildRecordsWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = serializers.InCompleteChildRecordsReadSerializer(
            self.child_record
        )
        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_child_record = self.get_object()
        self.child_record = serializer.save(updated_by=self.request.user)
        logger.debug(f"Incomplete Child Record({previous_child_record}) updated.")

        changes = incomplete_child_record_changes(
            previous_child_record, self.child_record
        )

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Incomplete Child Record(ID: {self.child_record.id}): {changes}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Incomplete Child Record(ID: {self.child_record.id}): {changes}) created."
        )


class DeleteInCompleteChildRecordsAPIView(generics.DestroyAPIView):
    queryset = InCompleteChildRecords.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.InCompleteChildRecordsWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        child_record_id = instance.id
        instance.delete()
        logger.debug(f"Incomplete Child Record({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Incomplete Child Record(ID: {child_record_id}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Incomplete Child Record(ID: {child_record_id}) was deleted by {self.request.user}) created."
        )

        # Delete associated flags
        delete_flag(instance, child_record_id, self.request.user)
