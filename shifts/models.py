import datetime

from django.contrib.auth.models import User
from django.db import models

from employees.models import Employee
from orgunits.models import Organization


class ShiftQuerySet(models.QuerySet):
    def filter_availability(self, occupancy_schedule):
        """TODO: Сделать фильтрацию по интервалам недельного календаря недоступностей сотрудника"""
        probe = self.filter(start__lte=occupancy_schedule['start_time'])

        return probe


class Shift(models.Model):
    objects = ShiftQuerySet.as_manager()
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

        prev = ShiftHistory.objects.filter(shift=self).last()
        reset = ShiftHistory.objects.create(shift=self)
        if not prev:
            reset.state_from = None
            reset.instance_diff['employee'] = {'from': None, 'to': None}

        else:
            reset.state_from = prev.state_to
            reset.instance_diff = {'employee': {'from': prev.instance_diff['employee']['to'], 'to': None}}
        reset.save()

        reset.user = user
        reset.party = 'party'
        reset.action = 'action'
        reset.state_to = 'Assign'
        reset.dt_created = datetime.datetime.now()
        reset.save()

        self.employee = employee
        self.save()

    def reset_employee(self, employee, user):
        """TODO: Сделать запись истории изменений"""
        prev = ShiftHistory.objects.filter(shift=self).last()
        reset = ShiftHistory.objects.create(shift=self)
        if not prev:
            reset.state_from = None
            reset.instance_diff['employee'] = {'from': None, 'to': None}

        else:
            reset.state_from = prev.state_to
            reset.instance_diff = {'employee': {'from': prev.instance_diff['employee']['to'], 'to': None}}
        reset.save()

        reset.user = user
        reset.party = 'party'
        reset.action = 'action'
        reset.state_to = 'Reset'
        reset.dt_created = datetime.datetime.now()
        reset.save()

        self.employee = employee
        self.save()


class ShiftHistory(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    party = models.CharField(max_length=24, default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь", null=True)
    action = models.CharField(max_length=124, default=None, null=True)
    state_from = models.CharField(max_length=24, default=None, null=True)
    state_to = models.CharField(max_length=24, default=None, null=True)
    instance_diff = models.JSONField(default=dict)
    dt_created = models.DateTimeField(blank=True, null=True, default=None)

    # {"change_history": [
    #     {
    #         "party": "employee",
    #         "user": {
    #             "username": employee_api.user.username,
    #             "email": employee_api.user.email,
    #         },
    #         "action": "assign_employee",
    #         "state_from": "open",
    #         "state_to": "assigned",
    #         "instance_diff": {
    #             "employee": {"to": employee_api.employee.id, "from": None},
    #         },
    #         "dt_created": "2021-03-08T00:00:00.000000+03:00",
    #     },}
