from rpas.models import Rpas
from rest_framework import serializers


class UserRPASListSerializer(serializers.ModelSerializer):

    rpas_name = serializers.SerializerMethodField()

    def get_rpas_name(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance:
            return str(instance.rpas_nickname)
        else:
            return None

    class Meta:
        model = Rpas
        fields = (
            "id",
            "rpas_name",
        )
