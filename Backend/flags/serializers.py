from rest_framework import serializers
from .models import Flags


class FlagWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flags
        fields = "__all__"


class FlagReadSerializer(serializers.ModelSerializer):
    content_type_display = serializers.StringRelatedField(
        source="content_type", read_only=True
    )
    flag_type_display = serializers.StringRelatedField(
        source="flag_type", read_only=True
    )
    created_by_display = serializers.StringRelatedField(
        source="created_by", read_only=True
    )
    updated_by_display = serializers.StringRelatedField(
        source="updated_by", read_only=True
    )

    class Meta:
        model = Flags
        fields = "__all__"
