from rest_framework import serializers
from .models import Absences
from api.models import CustomUser


class AbsencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Absences
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by_id = representation.pop("created_by", None)
        updated_by_id = representation.pop("updated_by", None)

        if created_by_id:
            created_by = CustomUser.objects.get(id=created_by_id).username
            representation.update({"created_by": created_by})

        if updated_by_id:
            updated_by = CustomUser.objects.get(id=updated_by_id).username
            representation.update({"updated_by": updated_by})

        return representation
