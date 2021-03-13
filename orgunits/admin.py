from django.contrib import admin

from orgunits.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "parent_name"]
    fields = ["name", "code", "parent"]
    autocomplete_fields = ["parent"]
    search_fields = ["name", "code"]
    readonly_fields = ["code"]

    def parent_name(self, obj):
        return obj.parent.name if obj.parent is not None else None

    parent_name.short_description = "Вышестоящая организация"
