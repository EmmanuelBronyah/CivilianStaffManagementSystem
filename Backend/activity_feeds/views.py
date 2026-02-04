from rest_framework import generics
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import ActivityFeeds
from django.db.models import F
from employees.views import LargeResultsSetPagination
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class ListActivityFeedAPIView(generics.ListAPIView):
    queryset = models.ActivityFeeds.objects.select_related("creator")
    serializer_class = serializers.ActivityFeedsSerializer
    permission_classes = [IsAuthenticated]


class SearchActivityAPIView(generics.ListAPIView):
    serializer_class = serializers.ActivityFeedsSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    @staticmethod
    def parse_date(date_str):
        try:
            if not date_str:
                return
            date_str = date_str.split()[0]
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return timezone.make_aware(dt)
        except ValueError:
            raise ValidationError({"detail": f"Invalid date format: {date_str}"})

    def get_queryset(self):
        q = self.request.query_params.get("q")
        start_date = self.parse_date(self.request.query_params.get("start_date"))
        end_date = self.parse_date(self.request.query_params.get("end_date"))

        qs = ActivityFeeds.objects.all()

        if q:
            search_query = SearchQuery(q, config="english")

            qs = (
                qs.annotate(rank=SearchRank(F("search_vector"), search_query))
                .filter(search_vector=search_query, rank__gte=0.1)
                .order_by("-rank")
            )

        if start_date:
            date = datetime.strptime(start_date, "%Y-%m-%d")
            qs = qs.filter(created_at__gte=date)

        if end_date:
            date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            qs = qs.filter(created_at__lt=date)

        return qs.order_by("-created_at")
