"""
Copyright 2021 ООО «Верме»
"""

from rest_framework import serializers

from orgunits.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "code", "parent"]
