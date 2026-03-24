from rpas.models import Rpas, RpasModel
from rest_framework import serializers


class UserRPASListSerializer(serializers.ModelSerializer):
    rpas_model_name = serializers.SerializerMethodField()

    def get_rpas_model_name(self, obj):
        if obj.rpas_model and obj.rpas_model.model_name:
            return obj.rpas_model.model_name
        return "Unknown Model"

    class Meta:
        model = Rpas
        fields = (
            "id",
            "cor_number",
            "rpas_serial",
            "rpas_model",
            "rpas_model_name",
        )


class UserRPASModelListSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SerializerMethodField()
    rpas_model_type = serializers.SerializerMethodField()

    def get_manufacturer(self, obj):
        if obj.manufacturer and obj.manufacturer.name:
            return obj.manufacturer.name
        return "Unknown Manufacturer"

    def get_rpas_model_type(self, obj):
        if obj.rpas_model_type and obj.rpas_model_type.airframe_type:
            return obj.rpas_model_type.airframe_type
        return "Unknown Model Type"

    class Meta:
        model = RpasModel
        fields = (
            "id",
            "model_name",
            "manufacturer",
            "rpas_model_type",
        )
