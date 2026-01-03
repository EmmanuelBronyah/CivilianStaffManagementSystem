from rest_framework import serializers
from .models import Children
from api.models import CustomUser
from employees.models import Gender


class ChildrenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Children
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by_id = representation.pop("created_by", None)
        updated_by_id = representation.pop("updated_by", None)
        gender_id = representation.pop("gender", None)

        if created_by_id:
            created_by = CustomUser.objects.get(id=created_by_id).username
            representation.update({"created_by": created_by})

        if updated_by_id:
            updated_by = CustomUser.objects.get(id=updated_by_id).username
            representation.update({"updated_by": updated_by})

        if gender_id:
            sex = Gender.objects.get(id=gender_id).sex
            representation.update({"gender": sex})

        return representation
