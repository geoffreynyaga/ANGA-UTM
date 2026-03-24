from django.contrib import admin
from .models import (
    DailyWorkLog,
    ChecklistTemplate,
)


class DailyWorkLogAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "user",
        "rpas",
        "is_complete",
        "reserve_airspace",
        "acres_sprayed",
        "bags_spread",
        # "preflight_template",
        # "postflight_template",
        "operation_date",
    )
    search_fields = ("project__name", "user__email")
    list_filter = ("operation_date", "user", "project")


admin.site.register(DailyWorkLog, DailyWorkLogAdmin)


class ChecklistTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "checklist_type",
        "rpas_model",
        "organization",
        "date_created",
    )
    list_filter = ("checklist_type", "organization")
    search_fields = ("title", "rpas_model__model_name")


admin.site.register(ChecklistTemplate, ChecklistTemplateAdmin)
