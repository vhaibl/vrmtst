import base64
import json
import random
import string

from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from orgunits.models import Organization


class DRFClient(APIClient):
    def __init__(
        self,
        god_mode=False,
        make_employee=False,
        anon=False,
        auth="token",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if not anon:
            self._create_user(god_mode, make_employee)
            self._auth(auth)

    def _auth(self, auth="token"):
        if auth == "token":
            token = (
                self.user.auth_token
                if hasattr(self.user, "auth_token") and self.user.auth_token
                else Token.objects.create(user=self.user)
            )
            self.credentials(
                HTTP_AUTHORIZATION=f"Token {token.key}", HTTP_X_CLIENT="testing",
            )
        elif auth == "basic":
            credentials = base64.b64encode(
                f"{self.user.username}:{self.password}".encode("utf-8"),
            )
            self.credentials(
                HTTP_AUTHORIZATION="Basic {}".format(credentials.decode("utf-8")),
            )
        else:
            pass

    def _create_user(self, god_mode=False, make_employee=False):
        user_opts = {"is_staff": False, "is_superuser": True} if god_mode else {}
        self.user = mixer.blend(get_user_model(), username=mixer.RANDOM, **user_opts)
        self.password = "".join([random.choice(string.hexdigits) for _ in range(0, 6)])
        self.user.set_password(self.password)
        self.user.save()
        if make_employee:
            self.organization = mixer.blend(Organization)
            self.employee = mixer.blend(
                "employees.Employee", user=self.user, organization=self.organization,
            )

    def logout(self):
        self.credentials()
        super().logout()

    def get(self, *args, **kwargs):
        return self._api_call(
            "get", kwargs.get("expected_status_code", 200), *args, **kwargs,
        )

    def post(self, *args, **kwargs):
        return self._api_call(
            "post", kwargs.get("expected_status_code", 201), *args, **kwargs,
        )

    def put(self, *args, **kwargs):
        return self._api_call(
            "put", kwargs.get("expected_status_code", 200), *args, **kwargs,
        )

    def patch(self, *args, **kwargs):
        return self._api_call(
            "patch", kwargs.get("expected_status_code", 200), *args, **kwargs,
        )

    def delete(self, *args, **kwargs):
        return self._api_call(
            "delete", kwargs.get("expected_status_code", 204), *args, **kwargs,
        )

    def _api_call(self, method, expected, *args, **kwargs):
        # by default submit all data in JSON
        kwargs["format"] = kwargs.get("format", "json")
        as_response = kwargs.pop("as_response", False)

        method = getattr(super(), method)
        response = method(*args, **kwargs)

        if as_response:
            return response

        content = self._decode(response)

        assert response.status_code == expected, content

        return content

    def _decode(self, response):
        if not len(response.content):
            return

        content = response.content.decode("utf-8", errors="ignore")
        if "application/json" in response._headers["content-type"][1]:
            return json.loads(content)
        else:
            return content
