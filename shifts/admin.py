from django.contrib import admin
from shifts.models import Shift, ShiftHistory


class HistoryInline(admin.TabularInline):
    model = ShiftHistory
    extra = 0

    def has_change_permission(self, request, obj):
        return False


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display =['start', 'end', 'state', 'employee', 'organization',]
    list_filter = ['state', 'organization']
    autocomplete_fields = ["employee", "organization"]
    search_fields = ["state", "organization__name", "employee__name"]
    inlines = [HistoryInline, ]
