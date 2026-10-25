from rest_framework import serializers

from inventory.models import (
    AircraftModel,
    ComponentRequest,
    ComponentType,
    ComponentUnit,
    StockLot,
    Tag,
)
from rpas.models import Rpas


class AircraftModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftModel
        fields = ("id", "manufacturer", "name")


class TagNamesField(serializers.ListField):
    """Tags are read and written as a list of names; unknown names are created."""

    child = serializers.CharField(max_length=40)

    def to_representation(self, value):
        return [tag.name for tag in value.all()]


class ComponentTypeSerializer(serializers.ModelSerializer):
    aircraft_models = serializers.PrimaryKeyRelatedField(
        many=True, queryset=AircraftModel.objects.all(), required=False
    )
    tags = TagNamesField(required=False)
    parent_name = serializers.CharField(source="parent.name", read_only=True)
    available = serializers.IntegerField(read_only=True)
    lot_quantity = serializers.IntegerField(read_only=True)
    available_units = serializers.IntegerField(read_only=True)
    unserviceable_units = serializers.IntegerField(read_only=True)
    has_stock_history = serializers.BooleanField(read_only=True)

    class Meta:
        model = ComponentType
        fields = (
            "id",
            "name",
            "part_number",
            "description",
            "image",
            "diagram_name",
            "diagram_number",
            "aircraft_models",
            "tags",
            "is_serialized",
            "parent",
            "parent_name",
            "status",
            "available",
            "lot_quantity",
            "available_units",
            "unserviceable_units",
            "has_stock_history",
        )
        read_only_fields = ("status", "diagram_name", "diagram_number")

    def _set_tags(self, component_type, names):
        tags = [Tag.objects.get_or_create(name=name.strip().lower())[0] for name in names]
        component_type.tags.set(tags)

    def create(self, validated_data):
        names = validated_data.pop("tags", [])
        component_type = super().create(validated_data)
        self._set_tags(component_type, names)
        return component_type

    def update(self, instance, validated_data):
        names = validated_data.pop("tags", None)
        component_type = super().update(instance, validated_data)
        if names is not None:
            self._set_tags(component_type, names)
        return component_type


class StockLotSerializer(serializers.ModelSerializer):
    source_rpas_name = serializers.StringRelatedField(source="source_rpas")

    class Meta:
        model = StockLot
        fields = (
            "id",
            "quantity",
            "condition",
            "origin",
            "source_rpas",
            "source_rpas_name",
            "date_created",
        )


class ComponentUnitSerializer(serializers.ModelSerializer):
    rpas_name = serializers.StringRelatedField(source="rpas")
    source_rpas_name = serializers.StringRelatedField(source="source_rpas")

    class Meta:
        model = ComponentUnit
        fields = (
            "id",
            "serial_number",
            "condition",
            "origin",
            "source_rpas",
            "source_rpas_name",
            "serviceable",
            "lifecycle",
            "rpas",
            "rpas_name",
            "last_serviced",
            "date_created",
        )
        read_only_fields = (
            "serial_number",
            "condition",
            "origin",
            "source_rpas",
            "rpas",
            "date_created",
        )

    def validate_lifecycle(self, value):
        # Other lifecycle changes go through requests and maintenance records
        if value not in (self.instance.lifecycle, ComponentUnit.SCRAPPED):
            raise serializers.ValidationError("Units can only be marked as scrapped here.")
        return value


class ComponentTypeDetailSerializer(ComponentTypeSerializer):
    lots = serializers.SerializerMethodField()
    units = serializers.SerializerMethodField()

    class Meta(ComponentTypeSerializer.Meta):
        fields = ComponentTypeSerializer.Meta.fields + ("lots", "units")

    def get_lots(self, obj):
        lots = obj.stock_lots.filter(organization=self.context["organization"])
        return StockLotSerializer(lots, many=True).data

    def get_units(self, obj):
        units = obj.units.filter(organization=self.context["organization"])
        return ComponentUnitSerializer(units, many=True).data


class AddStockSerializer(serializers.Serializer):
    component_type = serializers.PrimaryKeyRelatedField(
        queryset=ComponentType.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1, required=False)
    serial_numbers = serializers.ListField(
        child=serializers.CharField(max_length=60), required=False, allow_empty=False
    )
    condition = serializers.ChoiceField(
        choices=StockLot.CONDITION_CHOICES, default=StockLot.NEW
    )
    origin = serializers.ChoiceField(
        choices=StockLot.ORIGIN_CHOICES, default=StockLot.PURCHASED
    )
    source_rpas = serializers.PrimaryKeyRelatedField(
        queryset=Rpas.objects.all(), required=False, allow_null=True
    )
    last_serviced = serializers.DateField(required=False, allow_null=True)

    def validate(self, attrs):
        organization = self.context["organization"]
        component_type = attrs["component_type"]
        source_rpas = attrs.get("source_rpas")
        if source_rpas and source_rpas.organization_id != organization.pk:
            raise serializers.ValidationError(
                {"source_rpas": "The drone belongs to another organization."}
            )
        if component_type.is_serialized:
            serials = [s.strip() for s in attrs.get("serial_numbers", []) if s.strip()]
            if not serials:
                raise serializers.ValidationError(
                    {"serial_numbers": "Enter a serial number for each unit."}
                )
            if len(set(serials)) != len(serials):
                raise serializers.ValidationError(
                    {"serial_numbers": "Serial numbers must be unique."}
                )
            existing = ComponentUnit.objects.filter(
                organization=organization,
                component_type=component_type,
                serial_number__in=serials,
            ).values_list("serial_number", flat=True)
            if existing:
                raise serializers.ValidationError(
                    {"serial_numbers": f"Already in stock: {', '.join(existing)}"}
                )
            attrs["serial_numbers"] = serials
        elif not attrs.get("quantity"):
            raise serializers.ValidationError({"quantity": "Enter a quantity."})
        return attrs


class RpasSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Rpas
        fields = ("id", "name", "rpas_serial", "aircraft_model")

    def get_name(self, obj):
        return obj.rpas_nickname or obj.cor_number or obj.rpas_serial


class ComponentRequestSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source="component_type.name", read_only=True)
    rpas_name = serializers.SerializerMethodField()
    serial_number = serializers.CharField(source="unit.serial_number", read_only=True)
    requested_by_name = serializers.CharField(source="requested_by.get_full_name", read_only=True)
    decided_by_name = serializers.CharField(source="decided_by.get_full_name", read_only=True)

    class Meta:
        model = ComponentRequest
        fields = (
            "id",
            "component_type",
            "component_name",
            "rpas",
            "rpas_name",
            "lot",
            "unit",
            "serial_number",
            "quantity",
            "note",
            "status",
            "requested_by",
            "requested_by_name",
            "decided_by",
            "decided_by_name",
            "date_decided",
            "date_created",
        )
        read_only_fields = (
            "component_type",
            "status",
            "requested_by",
            "decided_by",
            "date_decided",
        )

    def get_rpas_name(self, obj):
        return RpasSerializer().get_name(obj.rpas)
