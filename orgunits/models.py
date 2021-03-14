"""
Copyright 2021 ООО «Верме»
"""
import uuid
from django.db import models


class OrganizationQuerySet(models.QuerySet):

    def tree_upwards(self, org_id):
        org = self.get(id=org_id)
        res = [org]
        if org.parent:

            next_parent = self.tree_upwards(org.parent.id)
            res += next_parent
        queryset = self.filter(id__in=[r.id for r in res])
        return queryset

    def tree_downwards(self, org_id):
        org = self.get(id=org_id)
        res = [org]
        children = self.filter(parent=org)
        if children:
            for child in children:
                res += self.tree_downwards(child.id)
        queryset = self.filter(id__in=[r.id for r in res])
        return queryset


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

    def parents(self):
        return OrganizationQuerySet(self).tree_upwards(self.id).exclude(id=self.id)

    def children(self):
        return OrganizationQuerySet(self).tree_downwards(self.id).exclude(id=self.id)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "организация"
        verbose_name = "организации"

    def __str__(self):
        return self.name
