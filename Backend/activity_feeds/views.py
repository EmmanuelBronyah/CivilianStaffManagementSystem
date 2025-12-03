from rest_framework import generics
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated


class ListActivityFeedAPIView(generics.ListAPIView):
    queryset = models.ActivityFeeds.objects.all()
    serializer_class = serializers.ActivityFeedsSerializer
    permission_classes = [IsAuthenticated]
