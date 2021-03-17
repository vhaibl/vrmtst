"""
Copyright 2021 ООО «Верме»
"""
import uuid
from django.db import models
from django.db.models.expressions import RawSQL


class OrganizationQuerySet(models.QuerySet):

    def tree_upwards(self, child_org_id):
        """ На основе https://developpaper.com/the-implementation-of-finding-all-child-nodes-by-sql-parent-node/ """

        query = '''
            WITH w1( id, parent_id, level) AS  
                (SELECT  
                    id,  
                    parent_id,  
                    0 AS level
                FROM  
                    orgunits_organization  
                WHERE  
                    id = %s 
                UNION ALL  
                SELECT  
                    orgunits_organization.id,  
                    orgunits_organization.parent_id,  
                    level + 1
                FROM  
                    orgunits_organization JOIN w1 ON orgunits_organization.id= w1.parent_id
                )  
            SELECT id FROM w1
            '''
        return self.filter(id__in=RawSQL(query, [child_org_id]))

    def tree_downwards(self, root_org_id):
        """ На основе https://developpaper.com/the-implementation-of-finding-all-child-nodes-by-sql-parent-node/ """

        query = '''
            WITH w1( id, parent_id) AS 
                (SELECT 
                    orgunits_organization.id, 
                    orgunits_organization.parent_id 
                FROM 
                    orgunits_organization 
                WHERE 
                    id = %s
                UNION ALL 
                SELECT 
                    orgunits_organization.id, 
                    orgunits_organization.parent_id 
                FROM 
                    orgunits_organization JOIN w1 ON orgunits_organization.parent_id= w1.id)
            SELECT id FROM w1
            '''
        return self.filter(id__in=RawSQL(query, [root_org_id]))

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
