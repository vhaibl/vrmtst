"""
Copyright 2021 ООО «Верме»
"""

from rest_framework import serializers

from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "number", "name", "user", "organization"]
