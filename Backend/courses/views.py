from rest_framework import generics
import logging
from . import serializers
from .models import Courses, IncompleteCourseRecords
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from employees.permissions import IsAdminUserOrStandardUser
from activity_feeds.models import ActivityFeeds
from django.shortcuts import get_object_or_404
from employees.models import Employee
from .utils import course_record_changes, incomplete_course_changes
from rest_framework.response import Response
from rest_framework import status
from flags.services import create_flag, delete_flag
from employees.views import LargeResultsSetPagination

logger = logging.getLogger(__name__)


class CreateCourseAPIView(generics.CreateAPIView):
    serializer_class = serializers.CoursesWriteSerializer
    queryset = Courses.objects.all()
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def create(self, request, *args, **kwargs):
        courses_data = request.data
        is_many = isinstance(courses_data, list)

        serializer = self.get_serializer(data=courses_data, many=is_many)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = serializers.CoursesReadSerializer(self.courses, many=is_many)

        return Response(read_serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.courses = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        records = (
            ", ".join([str(record) for record in self.courses])
            if isinstance(self.courses, list)
            else self.courses
        )
        logger.debug(f"Courses({records}) created.")

        if isinstance(self.courses, list):
            for record in self.courses:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=f"{self.request.user} added a new Course({record.course_type})",
                )
                logger.debug(
                    f"Activity Feed({self.request.user} added a new Course({record.course_type}) created."
                )
        else:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} added a new Course({self.courses.course_type})",
            )
            logger.debug(
                f"Activity Feed({self.request.user} added a new Course({self.courses.course_type}) created."
            )


class EditCourseAPIView(generics.UpdateAPIView):
    queryset = Courses.objects.all()
    serializer_class = serializers.CoursesWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = serializers.CoursesReadSerializer(self.courses_update)

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_courses = self.get_object()
        self.courses_update = serializer.save(updated_by=self.request.user)
        logger.debug(f"Courses({previous_courses}) updated.")

        changes = course_record_changes(previous_courses, self.courses_update)

        if changes:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=f"{self.request.user} updated Courses({previous_courses.course_type}): {changes}",
            )
            logger.debug(
                f"Activity Feed({self.request.user} updated Courses({previous_courses.course_type}): {changes}) created."
            )


class ListEmployeeCoursesAPIView(generics.ListAPIView):
    serializer_class = serializers.CoursesReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        courses = employee.courses.select_related("created_by", "updated_by")
        return courses


class RetrieveCourseAPIView(generics.RetrieveAPIView):
    queryset = Courses.objects.select_related("created_by", "updated_by")
    serializer_class = serializers.CoursesReadSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]


class DeleteCourseAPIView(generics.DestroyAPIView):
    queryset = Courses.objects.all()
    serializer_class = serializers.CoursesWriteSerializer
    lookup_field = "pk"
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def perform_destroy(self, instance):
        instance.delete()
        logger.debug(f"Course({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Course({instance.course_type}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Course({instance.course_type}) was deleted by {self.request.user}) created."
        )


# * INCOMPLETE COURSES
class CreateIncompleteCourseRecordsAPIView(generics.CreateAPIView):
    queryset = IncompleteCourseRecords.objects.all()
    serializer_class = serializers.IncompleteCourseRecordsWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        read_serializer = serializers.IncompleteCourseRecordsReadSerializer(self.course)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.course = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        logger.debug(f"Incomplete Course Record({self.course}) created.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} added a new Incomplete Course Record(ID: {self.course.id})",
        )
        logger.debug(
            f"Activity feed({self.request.user} added a new Incomplete Course Record(ID: {self.course.id})) created."
        )

        # Flag created record
        create_flag(self.course, self.request.user)


class RetrieveIncompleteCourseRecordsAPIView(generics.RetrieveAPIView):
    queryset = IncompleteCourseRecords.objects.select_related(
        "created_by", "updated_by"
    )
    lookup_field = "pk"
    serializer_class = serializers.IncompleteCourseRecordsReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]


class ListIncompleteCourseRecordsAPIView(generics.ListAPIView):
    queryset = IncompleteCourseRecords.objects.select_related(
        "created_by", "updated_by"
    )
    serializer_class = serializers.IncompleteCourseRecordsReadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class ListEmployeeIncompleteCourseRecordsAPIView(generics.ListAPIView):
    serializer_class = serializers.IncompleteCourseRecordsReadSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=service_id)
        incomplete_course_records = employee.incomplete_course_records.select_related(
            "created_by", "updated_by"
        )
        return incomplete_course_records


class EditIncompleteCourseRecordsAPIView(generics.UpdateAPIView):
    queryset = IncompleteCourseRecords.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.IncompleteCourseRecordsWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = serializers.IncompleteCourseRecordsReadSerializer(self.course)
        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_course = self.get_object()
        self.course = serializer.save(updated_by=self.request.user)
        logger.debug(f"Incomplete Course Record({previous_course}) updated.")

        changes = incomplete_course_changes(previous_course, self.course)

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{self.request.user} updated Incomplete Course Record(ID: {self.course.id}): {changes}",
        )
        logger.debug(
            f"Activity feed({self.request.user} updated Incomplete Course Record(ID: {self.course.id}): {changes}) created."
        )


class DeleteIncompleteCourseRecordsAPIView(generics.DestroyAPIView):
    queryset = IncompleteCourseRecords.objects.all()
    lookup_field = "pk"
    serializer_class = serializers.IncompleteCourseRecordsWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        course_id = instance.id
        instance.delete()
        logger.debug(f"Incomplete Course Record({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"The Incomplete Course Record(ID: {course_id}) was deleted by {self.request.user}",
        )
        logger.debug(
            f"Activity feed(The Incomplete Course Record(ID: {course_id}) was deleted by {self.request.user}) created."
        )

        # Delete associated flags
        delete_flag(instance, course_id, self.request.user)
