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

    def perform_create(self, serializer):
        flag = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )

        logger.debug(f"Flags({flag}) created.")

        model_name = flag.content_type.name.capitalize()

        flagged_field_text = (
            f" — Flagged Field: {flag.field.replace('_', ' ').capitalize()}"
            if flag.field
            else ""
        )

        ActivityFeeds.objects.create(
            creator=self.request.user,
            activity=(
                f"{model_name.replace('_', ' ').capitalize()} Record was flagged by {self.request.user}: "
                f"Flag Type: {flag.flag_type.flag_type}"
                f"{flagged_field_text}"
                f" — Reason: {flag.reason}"
            ),
        )
        logger.debug(
            f"Activity feed({model_name.replace('_', ' ').capitalize()} Record was flagged by {self.request.user}: "
            f"Flag Type: {flag.flag_type.flag_type}"
            f"{flagged_field_text}"
            f" — Reason: {flag.reason}"
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

    def perform_update(self, serializer):
        previous_flag = self.get_object()
        flag = serializer.save()
        logger.debug(f"Flags({previous_flag}) updated.")

        model_name = flag.content_type.name.capitalize()
        user = self.request.user

        changes_text = generate_changes_text(model_name, user, previous_flag, flag)

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
            activity=f"{model_name.replace('_', ' ').capitalize()} record flag was deleted by {self.request.user}. Flag Type: {instance.flag_type.flag_type.replace('_', ' ').capitalize() or 'None'} — Field: {instance.field.replace('_', ' ').capitalize() or 'None'} — Reason: {instance.reason or 'None'}",
        )
        logger.debug(
            f"Activity feed({model_name.replace('_', ' ').capitalize()} record flag was deleted by {self.request.user}. Flag Type: {instance.flag_type.flag_type.replace('_', ' ').capitalize() or 'None'} — Field: {instance.field.replace('_', ' ').capitalize() or 'None'} — Reason: {instance.reason or 'None'}) created."
        )
