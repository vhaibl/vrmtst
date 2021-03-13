import pytest
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
]


def test_get_employees_list_anonymous(anon):
    anon.get("/api/v1/employees/", expected_status_code=status.HTTP_401_UNAUTHORIZED)


def test_get_employees_list(basic_api, employee):
    assert basic_api.get("/api/v1/employees/") == [
        {
            "id": employee.id,
            "number": str(employee.number),
            "name": employee.name,
            "user": employee.user_id,
            "organization": employee.organization_id,
        },
    ]


def test_get_employees_detail(basic_api, employee):
    response = basic_api.get(f"/api/v1/employees/{employee.id}/")
    assert response == {
        "id": employee.id,
        "number": str(employee.number),
        "name": employee.name,
        "user": employee.user_id,
        "organization": employee.organization_id,
    }


def test_get_employees_self(employee_api):
    response = employee_api.get("/api/v1/employees/self/")
    assert response == {
        "id": employee_api.employee.id,
        "number": str(employee_api.employee.number),
        "name": employee_api.employee.name,
        "user": employee_api.employee.user_id,
        "organization": employee_api.employee.organization_id,
    }
