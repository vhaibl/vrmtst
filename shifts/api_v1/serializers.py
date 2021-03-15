"""
Copyright 2021 ООО «Верме»
"""
from django.contrib.auth.models import User
from rest_framework import serializers

from shifts.models import Shift, ShiftHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class StateHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    state = serializers.CharField(max_length=32, required=False)

    class Meta:
        model = ShiftHistory
        # fields = '__all__'
        exclude = ['id',]
    # pass


class ShiftSerializer(serializers.ModelSerializer):
    # change_history = StateHistorySerializer(read_only=True, many=True)
    class Meta:
        model = Shift
        fields = ["id", "organization", "employee", "start", "end", "state"]

    def create(self, validated_data):
        shift = Shift.objects.create(**validated_data, state='ope2n')
        # shift = Shift(state = 'open')
        # shift.employee = validated_data.get('employee')
        # shift.start = validated_data.get('start')
        # shift.end = validated_data.get('end')
        # shift.organization = validated_data.get('organization')
        # shift.save()
        return shift

class ShiftDetailSerializer(ShiftSerializer):
    change_history = StateHistorySerializer(read_only=True, many=True)
    state = serializers.CharField(max_length=32, required=False)
    class Meta:
        model = Shift

        fields = ["id", "organization", "employee", "start", "end", "state", "change_history"]

    def create(self, validated_data):
        shift = Shift.objects.create(**validated_data, state='ope2n')
        # shift = Shift(state = 'open')
        # shift.employee = validated_data.get('employee')
        # shift.start = validated_data.get('start')
        # shift.end = validated_data.get('end')
        # shift.organization = validated_data.get('organization')
        # shift.save()
        return shift
