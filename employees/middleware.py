from functools import lru_cache

from wfm.middleware import SimpleMiddleware


@lru_cache(maxsize=10)
def employee(self):
    if not self.user.is_anonymous and hasattr(self.user, "employee"):
        return self.user.employee


class EmployeeMiddleware(SimpleMiddleware):
    def __call__(self, request):
        request.__class__.employee = property(employee)

        return self.get_response(request)
