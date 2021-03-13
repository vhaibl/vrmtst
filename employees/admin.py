from django.contrib import admin

from employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "number", "user", "organization"]
    fields = ["number", "name", "user", "organization"]
    autocomplete_fields = ["organization", "user"]
    search_fields = ["name", "number", "user__name"]
    readonly_fields = ["number"]
    list_filter = ["organization"]
