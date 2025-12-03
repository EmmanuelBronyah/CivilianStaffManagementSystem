from rest_framework import serializers
from . import models
from api.models import CustomUser


class ActivityFeedsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ActivityFeeds
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        creator_id = representation.pop("creator", None)
        creator = CustomUser.objects.get(id=creator_id).username

        representation.update({"creator": creator})

        return representation
