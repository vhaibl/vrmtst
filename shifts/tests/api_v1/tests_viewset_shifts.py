import pytest
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
]


def test_get_shiftss_list_anonymous(anon):
    anon.get(
        "/api/v1/shifts/", expected_status_code=status.HTTP_401_UNAUTHORIZED,
    )


def test_get_shifts_list_empty(basic_api):
    assert basic_api.get("/api/v1/shifts/") == []


def test_get_shifts_list(tz, basic_api, shift):
    assert basic_api.get("/api/v1/shifts/") == [
        {
            "id": shift.id,
            "start": shift.start.astimezone(tz).isoformat(),
            "end": shift.end.astimezone(tz).isoformat(),
            "organization": shift.organization_id,
            "employee": shift.employee_id,
        },
    ]


def test_get_shifts_list_for_employee(tz, employee_api, shift, make_shift):
    shift_2 = make_shift(organization=employee_api.employee.organization)
    assert employee_api.get("/api/v1/shifts/") == [
        {
            "id": shift_2.id,
            "start": shift_2.start.astimezone(tz).isoformat(),
            "end": shift_2.end.astimezone(tz).isoformat(),
            "organization": shift_2.organization_id,
            "employee": shift_2.employee_id,
        },
    ]


def test_get_shifts_list_available(tz, employee_api, shift, make_shift):
    employee_api.employee.occupancy_schedule = [
        {"weekday": 1, "start_time": "00:00:00", "end_time": "1 00:00:00"},
    ]

    make_shift(
        organization=employee_api.employee.organization,
        start="2021-03-08T09:00:00+03:00",
        end="2021-03-08T18:00:00+03:00",
    )
    shift_3 = make_shift(
        organization=employee_api.employee.organization,
        start="2021-03-09T09:00:00+03:00",
        end="2021-03-09T18:00:00+03:00",
    )

    assert employee_api.get("/api/v1/shifts/available/") == [
        {
            "id": shift_3.id,
            "start": shift_3.start.astimezone(tz).isoformat(),
            "end": shift_3.end.astimezone(tz).isoformat(),
            "organization": shift_3.organization_id,
            "employee": shift_3.employee_id,
        },
    ]


def test_get_shift_by_employee(tz, employee_api, make_shift):
    shift = make_shift(organization=employee_api.employee.organization)
    assert employee_api.get(f"/api/v1/shifts/{shift.id}/") == {
            "id": shift.id,
            "start": shift.start.astimezone(tz).isoformat(),
            "end": shift.end.astimezone(tz).isoformat(),
            "organization": shift.organization_id,
            "employee": shift.employee_id,
            "change_history": [],
        }


@pytest.mark.freeze_time("2021-03-08T00:00:00.000000+03:00")
def test_get_shift_by_user(tz, basic_api, employee, make_shift):
    shift = make_shift(organization=employee.organization)
    shift.assign_employee(employee, basic_api.user)

    assert basic_api.get(f"/api/v1/shifts/{shift.id}/") == [
        {
            "id": shift.id,
            "start": shift.start.astimezone(tz).isoformat(),
            "end": shift.end.astimezone(tz).isoformat(),
            "organization": shift.organization_id,
            "employee": shift.employee_id,
            "change_history": [
                {
                    "party": "user",
                    "user": {
                        "username": basic_api.user.username,
                        "email": basic_api.user.email,
                    },
                    "action": "assign_employee",
                    "state_from": "open",
                    "state_to": "assigned",
                    "instance_diff": {"employee": {"to": employee.id, "from": None}},
                    "dt_created": "2021-03-08T00:00:00.000000+03:00",
                },
            ],
        },
    ]


@pytest.mark.freeze_time("2021-03-08T00:00:00.000000+03:00")
def test_book_shift_by_employee(tz, employee_api, make_shift):
    shift = make_shift(organization=employee_api.employee.organization)

    assert employee_api.put(f"/api/v1/shifts/{shift.id}/book/") == [
        {
            "id": shift.id,
            "start": shift.start.astimezone(tz).isoformat(),
            "end": shift.end.astimezone(tz).isoformat(),
            "organization": shift.organization_id,
            "employee": employee_api.employee.id,
            "change_history": [
                {
                    "party": "employee",
                    "user": {
                        "username": employee_api.user.username,
                        "email": employee_api.user.email,
                    },
                    "action": "assign_employee",
                    "state_from": "open",
                    "state_to": "assigned",
                    "instance_diff": {
                        "employee": {"to": employee_api.employee.id, "from": None},
                    },
                    "dt_created": "2021-03-08T00:00:00.000000+03:00",
                },
            ],
        },
    ]


@pytest.mark.freeze_time("2021-03-08T00:00:00.000000+03:00")
def test_refuse_shift_by_employee(tz, employee_api, make_shift):
    shift = make_shift(organization=employee_api.employee.organization)
    shift.assign_employee(employee_api.employee, employee_api.user)

    assert employee_api.put(f"/api/v1/shifts/{shift.id}/refuse/") == [
        {
            "id": shift.id,
            "start": shift.start.astimezone(tz).isoformat(),
            "end": shift.end.astimezone(tz).isoformat(),
            "organization": shift.organization_id,
            "employee": employee_api.employee.id,
            "change_history": [
                {
                    "party": "employee",
                    "user": {
                        "username": employee_api.user.username,
                        "email": employee_api.user.email,
                    },
                    "action": "reset_employee",
                    "state_from": "assigned",
                    "state_to": "open",
                    "instance_diff": {
                        "employee": {"to": None, "from": employee_api.employee.id},
                    },
                    "dt_created": "2021-03-08T00:00:00.000000+03:00",
                },
                {
                    "party": "employee",
                    "user": {
                        "username": employee_api.user.username,
                        "email": employee_api.user.email,
                    },
                    "action": "assign_employee",
                    "state_from": "open",
                    "state_to": "assigned",
                    "instance_diff": {
                        "employee": {"to": employee_api.employee.id, "from": None},
                    },
                    "dt_created": "2021-03-08T00:00:00.000000+03:00",
                },
            ],
        },
    ]
