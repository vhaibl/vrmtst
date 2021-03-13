import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from orgunits.models import Organization


class Employee(models.Model):
    """Сотрудник"""

    number = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, verbose_name="табельный номер",
    )
    name = models.CharField(max_length=250, verbose_name="ФИО")
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="пользователь",
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name="организация",
    )

    class Meta:
        unique_together = ("number", "organization")
        verbose_name_plural = "сотрудники"
        verbose_name = "сотрудник"

    def __str__(self):
        return self.name

    @property
    def occupancy_schedule(self):
        return

    @occupancy_schedule.setter
    def occupancy_schedule(self, schedule):
        """
        :type schedule: list
        """
