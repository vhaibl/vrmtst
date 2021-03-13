from django.contrib import admin

from shifts.models import Shift


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    """TODO: Сделать удобную админку для Смен (на свой вкус)"""
