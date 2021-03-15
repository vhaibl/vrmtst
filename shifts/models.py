import datetime

from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

from employees.models import Employee
from orgunits.models import Organization


class ShiftQuerySet(models.QuerySet):
    def filter_availability(self, occupancy_schedule):
        # zz = []
        # for x in occupancy_schedule:
        # datestart = datetime.datetime.strptime(x['start_time'], '%H:%M:%S')
        # dateend = datetime.datetime.strptime(x['end_time'], '%d %H:%M:%S')
        # weekday = x['weekday']
            # weekday = 0

        filter_weekday = self.exclude(start__iso_week_day__in=[a['weekday'] for a in occupancy_schedule])
        print([a['weekday'] for a in occupancy_schedule], 'okok')
        return filter_weekday


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
    state = models.CharField(max_length=16, blank=True, null=True, default='open')
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
        if user:
            party = 'user'
        else:
            party = 'employee'
        if not prev:
            reset.state_from = None
            reset.state_to = 'assigned'
            reset.instance_diff['employee'] = {'from': None, 'to': employee.id}

        else:
            reset.state_from = prev.state_to
            reset.instance_diff = {'employee': {'from': prev.instance_diff['employee']['to'], 'to': None}}
        reset.save()

        reset.user = user
        reset.party = party
        reset.action = 'assign_employee'
        reset.state_to = 'assigned'
        reset.dt_created = timezone.now()
        # reset.dt_created = datetime.datetime.now()
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
    shift = models.ForeignKey(Shift, related_name='change_history', on_delete=models.CASCADE)
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
