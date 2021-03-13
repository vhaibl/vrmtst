"""
Copyright 2020 ООО «Верме»
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from employees.api_v1.views import EmployeesViewSet
from orgunits.api_v1.views import OrganizationsViewSet
from shifts.api_v1.views import ShiftsViewSet

router = DefaultRouter()
router.register("organizations", OrganizationsViewSet)
router.register("employees", EmployeesViewSet)
router.register("shifts", ShiftsViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/token/", obtain_auth_token),
    path("api/v1/", include(router.urls)),
]
