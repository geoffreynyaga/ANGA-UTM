from rpas.models import Rpas
from rest_framework import serializers


class UserRPASListSerializer(serializers.ModelSerializer):


    class Meta:
        model = Rpas
        fields = (
            "id",
            "cor_number",
            "rpas_serial",
        )
