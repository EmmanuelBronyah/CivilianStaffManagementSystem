from rest_framework import generics
from .models import Occurrence
from .serializer import OccurrenceSerializer
from rest_framework.permissions import IsAuthenticated
from employees.permissions import IsAdminUserOrStandardUser
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
from activity_feeds.models import ActivityFeeds
import logging


logger = logging.getLogger(__name__)


class CreateOccurrenceAPIView(generics.CreateAPIView):
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer
    permission_classes = [IsAdminUserOrStandardUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):
        occurrence_data = request.data
        is_many = isinstance(occurrence_data, list)

        serializer = self.get_serializer(data=occurrence_data, many=is_many)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        occurrence = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )
        records = (
            ", ".join([str(record) for record in occurrence])
            if isinstance(occurrence, list)
            else occurrence
        )
        logger.debug(f"Occurrence({records}) created.")

        if isinstance(occurrence, list):
            for record in occurrence:
                ActivityFeeds.objects.create(
                    creator=self.request.user,
                    activity=(
                        f"{self.request.user} added a new occurrence: '{record.employee.service_id} — {record.authority} — {record.event}'"
                    ),
                )
        else:
            ActivityFeeds.objects.create(
                creator=self.request.user,
                activity=(
                    f"{self.request.user} added a new occurrence: '{occurrence.employee.service_id} — {occurrence.authority} — {occurrence.event}'"
                ),
            )
