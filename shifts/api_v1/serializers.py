"""
Copyright 2021 ООО «Верме»
"""

from rest_framework import serializers

from shifts.models import Shift, ShiftHistory


class StateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftHistory
        fields = '__all__'

    # pass


class ShiftSerializer(serializers.ModelSerializer):
    change_history = StateHistorySerializer(read_only=True, many=True)
    class Meta:
        model = Shift
        fields = ["id", "organization", "employee", "start", "end", "change_history"]


class ShiftDetailSerializer(ShiftSerializer):
    # change_history = StateHistorySerializer(read_only=True, many=True)

    class Meta:
        model = Shift

        fields = ["id", "organization", "employee", "start", "end"]
