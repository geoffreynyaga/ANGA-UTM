from django.contrib import admin

from .models import MaintenanceRecord


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("rpas", "service_type", "date_performed", "performed_by", "organization")
    list_filter = ("service_type", "organization")
    filter_horizontal = ("component_requests", "serviced_units")
