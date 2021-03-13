"""
Copyright 2021 ООО «Верме»
"""

from rest_framework.decorators import action

from orgunits.api_v1.serializers import OrganizationSerializer
from orgunits.models import Organization
from wfm.views import AnyAuthMixin
from wfm.viewsets import AppViewSet


class OrganizationsViewSet(AnyAuthMixin, AppViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    @action(methods=["GET"], detail=True)
    def parents(self, request, *args, **kwargs):
        """Возвращает родителей запрашиваемой организации
        TODO: Сделать метод API"""
        pass

    @action(methods=["GET"], detail=True)
    def children(self, request, *args, **kwargs):
        """Возвращает детей запрашиваемой организации
        TODO: Сделать метод API"""
        pass
