from rest_framework import serializers
from .models import ServiceWithForces, MilitaryRanks
from api.models import CustomUser
from employees.models import Units


class ServiceWithForcesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceWithForces
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by_id = representation.pop("created_by", None)
        updated_by_id = representation.pop("updated_by", None)
        last_unit_id = representation.pop("last_unit", None)
        military_rank_id = representation.pop("military_rank", None)

        if created_by_id:
            created_by = CustomUser.objects.get(id=created_by_id).username
            representation.update({"created_by": created_by})

        if updated_by_id:
            updated_by = CustomUser.objects.get(id=updated_by_id).username
            representation.update({"updated_by": updated_by})

        if last_unit_id:
            last_unit = Units.objects.get(id=last_unit_id).unit_name
            representation.update({"last_unit": last_unit})

        if military_rank_id:
            military_rank = MilitaryRanks.objects.get(id=military_rank_id).rank
            representation.update({"military_rank": military_rank})

        return representation


class MilitaryRanksSerializer(serializers.ModelSerializer):

    class Meta:
        model = MilitaryRanks
        fields = "__all__"
