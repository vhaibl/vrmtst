import datetime

from django.db.models import Q, F
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.utils.dateparse import parse_duration, parse_time

from employees.models import Employee
from orgunits.models import Organization


class ShiftQuerySet(models.QuerySet):
    def filter_availability(self, occupancy_schedule):

        z = []
        for o in occupancy_schedule:
            start_time = parse_time(o['start_time'])

            duration = parse_duration(o['end_time'])
            qo = self.exclude(start__iso_week_day=o['weekday'], start__time__gte=start_time, end__date__lte=F('start__time') + duration)
            z.append(qo.values_list('id', flat=True))

        queryset = self.filter(id__in=z)
        return queryset



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
    state = models.CharField(max_length=16, blank=True, null=True, default='open', verbose_name="Состояние")

    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"

    def __str__(self):
        return (
            f"{self.organization} / {self.start.isoformat()} - {self.end.isoformat()}"
        )

    def assign_employee(self, employee, user, party='user'):
        prev = ShiftHistory.objects.filter(shift=self).last()
        assign = ShiftHistory.objects.create(shift=self)
        if not prev:
            assign.state_from = 'open'
            assign.state_to = 'assigned'
            assign.instance_diff['employee'] = {'from': None, 'to': employee.id}
        else:
            assign.state_from = prev.state_to
            assign.instance_diff = {'employee': {'from': prev.instance_diff['employee']['to'], 'to': 'assigned'}}
        assign.save()
        assign.user = user
        assign.party = party
        assign.action = 'assign_employee'
        assign.state_to = 'assigned'
        assign.dt_created = timezone.now()
        assign.save()
        self.state = 'assigned'
        self.employee = employee
        self.save()

    def reset_employee(self, employee, user, party='user'):
        prev = ShiftHistory.objects.filter(shift=self).last()
        reset = ShiftHistory.objects.create(shift=self)
        if not prev:
            reset.state_from = None
            reset.instance_diff['employee'] = {'from': 'open', 'to': 'open'}

        else:
            reset.state_from = prev.state_to
            reset.instance_diff = {'employee': {'from': prev.instance_diff['employee']['to'], 'to': None}}
        reset.save()
        reset.user = user
        reset.party = party
        reset.action = 'reset_employee'
        reset.state_to = 'open'
        reset.dt_created = timezone.now()
        reset.save()
        self.state = 'open'
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

    class Meta:
        ordering = ['-id']
