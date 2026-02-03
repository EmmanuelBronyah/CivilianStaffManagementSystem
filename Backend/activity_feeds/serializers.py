from rest_framework import serializers
from . import models


class ActivityFeedsSerializer(serializers.ModelSerializer):
    creator_display = serializers.StringRelatedField(source="creator", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", read_only=True)

    class Meta:
        model = models.ActivityFeeds
        exclude = ("search_vector",)
