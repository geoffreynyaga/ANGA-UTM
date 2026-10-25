from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import (
    AircraftModel,
    ComponentRequest,
    ComponentType,
    ComponentUnit,
    StockLot,
    Tag,
)


@admin.register(AircraftModel)
class AircraftModelAdmin(admin.ModelAdmin):
    list_display = ("manufacturer", "name")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(ComponentType)
class ComponentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "part_number", "status", "is_serialized", "parent")
    list_filter = ("status", "is_serialized", "aircraft_models")
    search_fields = ("name", "part_number", "tags__name")
    filter_horizontal = ("aircraft_models", "tags")
    actions = ("merge_into_approved",)

    @admin.action(description="Merge selected pending types into the selected approved type")
    def merge_into_approved(self, request, queryset):
        approved = queryset.filter(status=ComponentType.APPROVED)
        pending = queryset.filter(status=ComponentType.PENDING)
        if approved.count() != 1 or not pending.exists():
            self.message_user(
                request,
                "Select exactly one approved type and at least one pending type.",
                messages.ERROR,
            )
            return
        target = approved.get()
        try:
            for duplicate in pending:
                duplicate.merge_into(target)
        except ValidationError as error:
            self.message_user(request, error.messages[0], messages.ERROR)
            return
        self.message_user(request, f"Merged into {target}.")


@admin.register(StockLot)
class StockLotAdmin(admin.ModelAdmin):
    list_display = ("component_type", "organization", "quantity", "condition", "origin")
    list_filter = ("condition", "origin", "organization")
    search_fields = ("component_type__name", "component_type__part_number")


@admin.register(ComponentUnit)
class ComponentUnitAdmin(admin.ModelAdmin):
    list_display = (
        "component_type",
        "serial_number",
        "organization",
        "lifecycle",
        "serviceable",
        "rpas",
        "last_serviced",
    )
    list_filter = ("lifecycle", "serviceable", "condition", "organization")
    search_fields = ("serial_number", "component_type__name")


@admin.register(ComponentRequest)
class ComponentRequestAdmin(admin.ModelAdmin):
    list_display = (
        "component_type",
        "quantity",
        "rpas",
        "status",
        "requested_by",
        "decided_by",
        "date_created",
    )
    list_filter = ("status", "organization")
