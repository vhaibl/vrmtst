"""
Copyright 2021 ООО «Верме»
"""

from rest_framework import serializers

from shifts.models import Shift


class StateHistorySerializer(serializers.Serializer):
    pass


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ["id", "organization", "employee", "start", "end"]


class ShiftDetailSerializer(ShiftSerializer):
    state_history = StateHistorySerializer(read_only=True, many=True)

    class Meta:
        model = Shift
        fields = ["id", "organization", "employee", "start", "end", "state_history"]
