from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from shifts.api_v1.serializers import ShiftDetailSerializer, ShiftSerializer
from shifts.models import Shift
from wfm.views import AnyAuthMixin
from wfm.viewsets import AppViewSet


class ShiftsViewSet(AnyAuthMixin, AppViewSet):
    serializer_class = ShiftDetailSerializer
    serializer_action_classes = {
        "list": ShiftSerializer,
        "available": ShiftSerializer,
    }
    queryset = Shift.objects.all()
    filter_backends = []

    def get_queryset(self):
        if self.request.employee:
            return Shift.objects.filter(organization=self.request.employee.organization)
        else:
            return Shift.objects.all()

    @action(methods=["GET"], detail=False)
    def available(self, request, *args, **kwargs):
        """Возвращает смены с учётом графика доступности"""
        if not request.employee:
            raise ValidationError("Запрос должен производиться сотрудником")
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter_availability(request.employee.occupancy_schedule)
        print(request.employee.occupancy_schedule, 'in view')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["PUT"], detail=True)
    def book(self, request, *args, **kwargs):
        if not request.employee:
            raise ValidationError("Запрос должен производиться сотрудником")
        shift = self.get_object()
        shift.assign_employee(request.employee, request.user)
        serializer = self.get_serializer(shift)
        return Response(serializer.data)

    @action(methods=["PUT"], detail=True)
    def refuse(self, request, *args, **kwargs):
        if not request.employee:
            raise ValidationError("Запрос должен производиться сотрудником")
        shift = self.get_object()
        shift.reset_employee(request.employee, request.user)
        serializer = self.get_serializer(shift)
        return Response(serializer.data)
