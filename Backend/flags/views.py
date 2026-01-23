from rest_framework import generics
from .serializers import FlagReadSerializer, FlagWriteSerializer
from .models import Flags
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
import logging
from activity_feeds.models import ActivityFeeds
from employees.permissions import IsAdminUserOrStandardUser
from employees.views import LargeResultsSetPagination
from .utils import generate_changes_text


logger = logging.getLogger(__name__)


class CreateFlagsAPIView(generics.CreateAPIView):
    queryset = Flags.objects.all()
    serializer_class = FlagWriteSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        read_serializer = FlagReadSerializer(self.flag)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        self.flag = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )

        logger.debug(f"Flags({self.flag}) created.")

        model_name = self.flag.content_type.name.capitalize()

        flagged_field_text = (
            f" — Flagged Field: {self.flag.field.replace('_', ' ').capitalize()}"
            if self.flag.field
            else ""
        )

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=(
                f"{model_name.replace('_', ' ').capitalize()} was flagged by {self.request.user}: "
                f"Flag Type: {self.flag.flag_type.flag_type}"
                f"{flagged_field_text}"
                f" — Reason: {self.flag.reason}"
            ),
        )
        logger.debug(
            f"Activity feed({model_name.replace('_', ' ').capitalize()} was flagged by {self.request.user}: "
            f"Flag Type: {self.flag.flag_type.flag_type}"
            f"{flagged_field_text}"
            f" — Reason: {self.flag.reason}"
        )


class RetrieveFlagAPIView(generics.RetrieveAPIView):
    queryset = Flags.objects.select_related(
        "flag_type", "content_type", "created_by", "updated_by"
    )
    lookup_field = "pk"
    serializer_class = FlagReadSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ListFlagsAPIView(generics.ListAPIView):
    queryset = Flags.objects.select_related(
        "flag_type", "content_type", "created_by", "updated_by"
    )
    serializer_class = FlagReadSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination


class EditFlagsAPIView(generics.UpdateAPIView):
    queryset = Flags.objects.all()
    lookup_field = "pk"
    serializer_class = FlagWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        read_serializer = FlagReadSerializer(self.flag)

        return Response(read_serializer.data)

    def perform_update(self, serializer):
        previous_flag = self.get_object()
        self.flag = serializer.save()
        logger.debug(f"Flags({previous_flag}) updated.")

        model_name = self.flag.content_type.name.capitalize()
        user = self.request.user

        changes_text = generate_changes_text(model_name, user, previous_flag, self.flag)

        ActivityFeeds.objects.create(creator=self.request.user, activity=changes_text)
        logger.debug(f"Activity feed({changes_text})")


class DeleteFlagsAPIView(generics.DestroyAPIView):
    queryset = Flags.objects.all()
    lookup_field = "pk"
    serializer_class = FlagWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]
    throttle_classes = [UserRateThrottle]

    def perform_destroy(self, instance):
        model_name = instance.content_type.name.capitalize()
        instance.delete()
        logger.debug(f"Flags({instance}) deleted.")

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=f"{model_name.replace('_', ' ').capitalize()} flag was deleted by {self.request.user}. Flag Type: {instance.flag_type.flag_type.replace('_', ' ').capitalize() or 'None'} — Field: {instance.field.replace('_', ' ').capitalize() or 'None'} — Reason: {instance.reason or 'None'}",
        )
        logger.debug(
            f"Activity feed({model_name.replace('_', ' ').capitalize()} flag was deleted by {self.request.user}. Flag Type: {instance.flag_type.flag_type.replace('_', ' ').capitalize() or 'None'} — Field: {instance.field.replace('_', ' ').capitalize() or 'None'} — Reason: {instance.reason or 'None'}) created."
        )
