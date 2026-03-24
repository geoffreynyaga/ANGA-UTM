from rest_framework import serializers
from administration.models import FieldExpense, FieldRequisition


class FieldExpenseSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = FieldExpense
        fields = "__all__"
        read_only_fields = ("duration_days", "user", "date_created", "date_modified")


class FieldRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldRequisition
        fields = "__all__"
        read_only_fields = ("duration_days", "user", "date_created", "date_modified")
