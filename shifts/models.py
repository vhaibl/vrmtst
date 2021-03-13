from django.db import models

from employees.models import Employee
from orgunits.models import Organization


class ShiftQuerySet(models.QuerySet):
    def filter_availability(self, occupancy_schedule):
        """TODO: Сделать фильтрацию по интервалам недельного календаря недоступностей сотрудника"""
        return self.none()


class Shift(models.Model):
    start = models.DateTimeField(verbose_name="Начало")
    end = models.DateTimeField(verbose_name="Окончание")
    employee = models.ForeignKey(
        Employee,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Сотрудник",
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name="Организация",
    )

    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"

    def __str__(self):
        return (
            f"{self.organization} / {self.start.isoformat()} - {self.end.isoformat()}"
        )

    def assign_employee(self, employee, user):
        """TODO: Сделать запись истории изменений"""
        self.employee = employee
        self.save()

    def reset_employee(self, employee, user):
        """TODO: Сделать запись истории изменений"""
        self.employee = employee
        self.save()
