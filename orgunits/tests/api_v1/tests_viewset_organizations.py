import pytest
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
]


def test_get_organizations_list_anonymous(anon):
    anon.get(
        "/api/v1/organizations/", expected_status_code=status.HTTP_401_UNAUTHORIZED,
    )


def test_get_organizations_list_empty(basic_api):
    assert basic_api.get("/api/v1/organizations/") == []


def test_get_organizations_list(basic_api, organization):
    assert basic_api.get("/api/v1/organizations/") == [
        {
            "id": organization.id,
            "name": organization.name,
            "code": str(organization.code),
            "parent": organization.parent_id,
        },
    ]


def test_get_organization_detail(basic_api, organization):
    response = basic_api.get(f"/api/v1/organizations/{organization.id}/")
    assert response == {
        "id": organization.id,
        "name": organization.name,
        "code": str(organization.code),
        "parent": organization.parent_id,
    }


def test_get_organization_detail_with_parent_id(basic_api, make_organization):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    response = basic_api.get(f"/api/v1/organizations/{org_2.id}/")
    assert response == {
        "id": org_2.id,
        "name": org_2.name,
        "code": str(org_2.code),
        "parent": org_1.id,
    }


def test_get_organization_parents(basic_api, make_organization):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    response = basic_api.get(f"/api/v1/organizations/{org_2.id}/parents/")
    assert response == [
        {
            "id": org_1.id,
            "name": org_1.name,
            "code": str(org_1.code),
            "parent": org_1.parent_id,
        },
    ]


def test_get_organization_children(basic_api, make_organization):
    org_1 = make_organization()
    org_2 = make_organization(parent=org_1)
    response = basic_api.get(f"/api/v1/organizations/{org_1.id}/children/")
    assert response == [
        {
            "id": org_2.id,
            "name": org_2.name,
            "code": str(org_2.code),
            "parent": org_2.parent_id,
        },
    ]
