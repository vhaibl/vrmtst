"""
Copyright 2021 ООО «Верме»
"""
import uuid

from django.db import models


class OrganizationQuerySet(models.QuerySet):
    """TODO: Сделать методы для работы с деревом или использовать готовую библиотеку"""


class Organization(models.Model):
    """Организации"""

    objects = OrganizationQuerySet.as_manager()

    code = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, verbose_name="код",
    )
    name = models.CharField(max_length=250, verbose_name="наименование")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="вышестоящая организация",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "организация"
        verbose_name = "организации"

    def __str__(self):
        return self.name
