from django.db.models import Count, Max
from django.templatetags.static import static
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.api.views import InventoryAPIView, run_model_action
from inventory.models import ComponentRequest
from maintenance.api.serializers import (
    MaintenanceRecordSerializer,
    MaintenanceRpasSerializer,
)
from maintenance.models import MaintenanceRecord
from rpas.models import Rpas


class MaintenanceRecordListCreateAPIView(InventoryAPIView, generics.ListCreateAPIView):
    serializer_class = MaintenanceRecordSerializer

    def get_queryset(self):
        queryset = (
            MaintenanceRecord.objects.filter(organization=self.organization)
            .select_related("rpas", "performed_by")
            .prefetch_related(
                "component_requests__component_type",
                "component_requests__unit",
                "serviced_units__component_type",
            )
        )
        rpas = self.request.query_params.get("rpas")
        if rpas:
            queryset = queryset.filter(rpas_id=rpas)
        return queryset

    def perform_create(self, serializer):
        self.require_organization()
        data = dict(serializer.validated_data)
        serializer.instance = run_model_action(
            MaintenanceRecord.record, performed_by=self.request.user, **data
        )


class MaintenanceRecordDetailAPIView(InventoryAPIView, generics.RetrieveAPIView):
    serializer_class = MaintenanceRecordSerializer

    def get_queryset(self):
        return MaintenanceRecord.objects.filter(organization=self.organization)


class MaintenanceRpasListAPIView(InventoryAPIView, generics.ListAPIView):
    """Drones with the date of their latest maintenance record."""

    serializer_class = MaintenanceRpasSerializer

    def get_queryset(self):
        return Rpas.objects.filter(organization=self.organization).annotate(
            last_serviced=Max("maintenance_records__date_performed"),
            record_count=Count("maintenance_records"),
        )


class InstallableRequestListAPIView(InventoryAPIView, APIView):
    """Approved requests for a drone that can be recorded as fitted."""

    def get(self, request, *args, **kwargs):
        requests = ComponentRequest.objects.filter(
            organization=self.organization,
            status=ComponentRequest.APPROVED,
            rpas_id=request.query_params.get("rpas"),
        ).select_related("component_type", "unit")
        return Response(
            [
                {
                    "id": r.pk,
                    "component_name": r.component_type.name,
                    "serial_number": r.unit.serial_number if r.unit_id else None,
                    "quantity": r.quantity,
                }
                for r in requests
            ]
        )


class ReportTemplateAPIView(InventoryAPIView, APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {"url": static("maintenance/maintenance_report_template.docx")}
        )
