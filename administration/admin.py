from django.contrib import admin
from .models import FieldExpense, FieldRequisition

# Register your models here.


@admin.register(FieldExpense)
class FieldExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "project",
        "category",
        "start_date",
        "end_date",
        "duration_days",
        "date_created",
    )
    list_filter = ("category", "date_created", "date_modified")
    search_fields = ("user__username", "project__name", "description")
    readonly_fields = ("duration_days", "date_created", "date_modified")
    date_hierarchy = "start_date"


@admin.register(FieldRequisition)
class FieldRequisitionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "project",
        "category",
        "start_date",
        "end_date",
        "duration_days",
        "status",
        "approved_by",
        "date_created",
    )
    list_filter = ("category", "status", "date_created", "date_modified")
    search_fields = ("user__username", "project__name", "description", "status_message")
    readonly_fields = ("duration_days", "date_created", "date_modified")
    date_hierarchy = "start_date"
    actions = ["approve_requisitions", "reject_requisitions"]

    def approve_requisitions(self, request, queryset):
        for requisition in queryset:
            requisition.status = "APPROVED"
            requisition.approved_by = request.user
            requisition.approved_date = timezone.now()
            requisition.save()
        self.message_user(request, f"Approved {queryset.count()} requisitions.")

    approve_requisitions.short_description = "Approve selected requisitions"

    def reject_requisitions(self, request, queryset):
        for requisition in queryset:
            requisition.status = "REJECTED"
            requisition.approved_by = request.user
            requisition.approved_date = timezone.now()
            requisition.save()
        self.message_user(request, f"Rejected {queryset.count()} requisitions.")

    reject_requisitions.short_description = "Reject selected requisitions"
