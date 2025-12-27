from rest_framework import serializers
from .models import Occurrence, LevelStep, SalaryAdjustmentPercentage, Event


class OccurrenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Occurrence
        fields = "__all__"


class LevelStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = LevelStep
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"


class SalaryAdjustmentPercentageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalaryAdjustmentPercentage
        fields = "__all__"
