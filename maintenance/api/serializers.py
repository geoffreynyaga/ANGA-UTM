from rest_framework import serializers

from inventory.api.serializers import RpasSerializer
from inventory.models import ComponentRequest, ComponentUnit
from maintenance.models import MaintenanceRecord
from rpas.models import Rpas


class UsedComponentSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source="component_type.name", read_only=True)
    part_number = serializers.CharField(source="component_type.part_number", read_only=True)
    serial_number = serializers.CharField(source="unit.serial_number", read_only=True)

    class Meta:
        model = ComponentRequest
        fields = ("id", "component_name", "part_number", "serial_number", "quantity", "status")


class ServicedUnitSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source="component_type.name", read_only=True)

    class Meta:
        model = ComponentUnit
        fields = ("id", "component_name", "serial_number", "last_serviced")


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    rpas_name = serializers.SerializerMethodField()
    performed_by_name = serializers.CharField(
        source="performed_by.get_full_name", read_only=True
    )
    component_requests = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ComponentRequest.objects.all(), required=False
    )
    serviced_units = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ComponentUnit.objects.all(), required=False
    )
    components_used = UsedComponentSerializer(
        source="component_requests", many=True, read_only=True
    )
    units_serviced = ServicedUnitSerializer(
        source="serviced_units", many=True, read_only=True
    )

    class Meta:
        model = MaintenanceRecord
        fields = (
            "id",
            "rpas",
            "rpas_name",
            "performed_by",
            "performed_by_name",
            "date_performed",
            "service_type",
            "description",
            "report",
            "component_requests",
            "serviced_units",
            "components_used",
            "units_serviced",
            "date_created",
        )
        read_only_fields = ("performed_by",)

    def get_rpas_name(self, obj):
        return RpasSerializer().get_name(obj.rpas)


class MaintenanceRpasSerializer(RpasSerializer):
    last_serviced = serializers.DateField(read_only=True)
    record_count = serializers.IntegerField(read_only=True)

    class Meta(RpasSerializer.Meta):
        model = Rpas
        fields = RpasSerializer.Meta.fields + ("last_serviced", "record_count")
