from rest_framework.generics import get_object_or_404

from employees.api_v1.serializers import EmployeeSerializer
from employees.models import Employee
from wfm.views import AnyAuthMixin
from wfm.viewsets import AppViewSet


class EmployeesViewSet(AnyAuthMixin, AppViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = (
            {"user": self.request.user}
            if self.kwargs["pk"] == "self"
            else {"pk": self.kwargs["pk"]}
        )
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
