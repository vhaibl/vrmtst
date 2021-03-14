"""
Copyright 2021 ООО «Верме»
"""

from rest_framework.decorators import action
from rest_framework.response import Response

from orgunits.api_v1.serializers import OrganizationSerializer
from orgunits.models import Organization
from wfm.views import AnyAuthMixin
from wfm.viewsets import AppViewSet


class OrganizationsViewSet(AnyAuthMixin, AppViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    @action(methods=["GET"], detail=True)
    def parents(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = Organization(pk).parents()
        data = self.get_serializer(instance, many=True).data
        return Response(data)

    @action(methods=["GET"], detail=True)
    def children(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = Organization(pk).children()
        data = self.get_serializer(instance, many=True).data
        return Response(data)
