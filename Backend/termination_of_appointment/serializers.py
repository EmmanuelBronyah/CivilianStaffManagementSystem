from rest_framework import serializers
from . import models
from api.models import CustomUser


class TerminationOfAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TerminationOfAppointment
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by_id = representation.pop("created_by", None)
        updated_by_id = representation.pop("updated_by", None)
        cause_of_termination_id = representation.pop("cause", None)
        termination_status_id = representation.pop("status", None)

        if created_by_id:
            created_by = CustomUser.objects.get(id=created_by_id).username
            representation.update({"created_by": created_by})

        if updated_by_id:
            updated_by = CustomUser.objects.get(id=updated_by_id).username
            representation.update({"updated_by": updated_by})

        if cause_of_termination_id:
            cause = models.CausesOfTermination.objects.get(
                id=cause_of_termination_id
            ).cause
            representation.update({"cause": cause})

        if termination_status_id:
            termination_status = models.TerminationStatus.objects.get(
                id=termination_status_id
            ).termination_status
            representation.update({"status": termination_status})

        return representation


class CausesOfTerminationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CausesOfTermination
        fields = "__all__"


class TerminationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TerminationStatus
        fields = "__all__"
