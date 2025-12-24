from rest_framework import serializers
from .models import Flags
from api.models import CustomUser
from django.contrib.contenttypes.models import ContentType


class FlagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flags
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by_id = representation.pop("created_by", None)
        updated_by_id = representation.pop("updated_by", None)

        content_type = representation.pop("content_type", None)

        if created_by_id:
            created_by = CustomUser.objects.get(id=created_by_id).username
            representation.update({"created_by": created_by})

        if updated_by_id:
            updated_by = CustomUser.objects.get(id=updated_by_id).username
            representation.update({"updated_by": updated_by})

        if content_type:
            model_name = ContentType.objects.get(id=content_type).name
            representation.update({"content_type": model_name.capitalize()})

        return representation
