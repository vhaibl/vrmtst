"""
Copyright 2020 ООО «Верме»
"""

import pytest
from django.utils import timezone

from employees.models import Employee
from orgunits.models import Organization
from wfm.test import mixer as _mixer
from wfm.test.api_client import DRFClient
from wfm.test.view_client import ViewClient

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture()
def tz():
    return timezone.get_current_timezone()


@pytest.fixture()
def anon(db):
    return DRFClient(anon=True)


@pytest.fixture()
def mixer():
    return _mixer


@pytest.fixture()
def session_api(db, settings):
    return ViewClient()


@pytest.fixture()
def basic_api(db, settings):
    return DRFClient(auth="basic")


@pytest.fixture()
def employee_api(settings):
    return DRFClient(make_employee=True)


@pytest.fixture()
def make_employee(mixer):
    def _organization_generator(**kwargs):
        return mixer.blend(Employee, **kwargs)

    return _organization_generator


@pytest.fixture()
def employee(make_employee):
    return make_employee()


@pytest.fixture()
def make_organization(mixer):
    def _organization_generator(**kwargs):
        return mixer.blend(Organization, **kwargs)

    return _organization_generator


@pytest.fixture()
def organization(make_organization):
    return make_organization()
