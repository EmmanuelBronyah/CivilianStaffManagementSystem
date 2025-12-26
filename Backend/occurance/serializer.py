from rest_framework import serializers
from .models import Occurrence, LevelStep, SalaryPercentageAdjustment


class OccurrenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Occurrence
        fields = "__all__"


class LevelStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = LevelStep
        fields = "__all__"


class SalaryPercentageAdjustmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalaryPercentageAdjustment
        fields = "__all__"
