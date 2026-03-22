from applications.models import ReserveAirspace
from rest_framework import serializers
from flight_plans.models import ChecklistTemplate, DailyWorkLog


class FlightLogReserveAirspaceSerializer(serializers.ModelSerializer):
    rpas_name = serializers.SerializerMethodField()
    mission_type_display = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    start_datetime = serializers.SerializerMethodField()

    def get_rpas_name(self, instance):
        if instance.rpas:
            return str(instance.rpas.rpas_nickname)
        return None

    def get_mission_type_display(self, obj):
        return obj.get_mission_type_display()

    def get_area(self, obj):
        return obj.get_area()

    def get_start_datetime(self, obj):
        return obj.get_start_datetime()

    class Meta:
        model = ReserveAirspace
        fields = (
            "rpas_name",
            "start_day",
            "start_time",
            "end",
            "application_number",
            "status",
            "start_datetime",
            "area",
            "mission_type_display",
        )


class FlightLogListSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)
    reserve_airspace = FlightLogReserveAirspaceSerializer(read_only=True)
    post_flight_completion = serializers.SerializerMethodField()
    pre_flight_completion = serializers.SerializerMethodField()

    def get_post_flight_completion(self, obj):
        return obj.get_post_flight_completion()

    def get_pre_flight_completion(self, obj):
        return obj.get_pre_flight_completion()

    class Meta:
        model = DailyWorkLog
        fields = (
            "id",
            "user_first_name",
            "user_last_name",
            "reserve_airspace",
            "post_flight_completion",
            "pre_flight_completion",
        )


class CheckListDetailSerializer(serializers.ModelSerializer):
    # This now directly returns the React-friendly JSON blob
    class Meta:
        model = ChecklistTemplate
        fields = (
            "id",
            "title",
            "checklist_type",
            "checklist_data",
            "rpas_model",
            "date_created",
        )


class CheckListTemplateListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )
    organization = serializers.CharField(source="organization.name", read_only=True)
    rpas_model = serializers.CharField(source="rpas_model.model_name", read_only=True)

    class Meta:
        model = ChecklistTemplate
        fields = (
            "id",
            "title",
            "checklist_type",
            "date_created",
            "rpas_model",
            "organization",
            # "checklist_data",
            "created_by",
        )


class WorkLogDetailSerializer(serializers.ModelSerializer):

    preflight_template = CheckListDetailSerializer(read_only=True)
    postflight_template = CheckListDetailSerializer(read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    rpas_name = serializers.CharField(source="rpas.cor_number", read_only=True)

    class Meta:
        model = DailyWorkLog
        fields = (
            "id",
            "user",
            "rpas",
            "project",
            "project_name",
            "rpas_name",
            "reserve_airspace",
            "acres_sprayed",
            "bags_spread",
            "application_rate_spraying",
            "operation_date",
            "organization",
            "preflight_template",
            "postflight_template",
            "is_complete",
        )


class WorkLogListSerializer(serializers.ModelSerializer):
    rpas_cor_number = serializers.CharField(source="rpas.cor_number", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = DailyWorkLog
        fields = (
            "id",
            "user",
            "rpas",
            "acres_sprayed",
            "bags_spread",
            "application_rate_spraying",
            "operation_date",
            "organization",
            "preflight_template",
            "postflight_template",
            "is_complete",
            "rpas_cor_number",
            "project_name",
        )
