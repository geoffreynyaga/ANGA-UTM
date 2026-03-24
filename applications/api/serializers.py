from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoModelSerializer
from applications.models import Project, ReserveAirspace
from rpas.models import Rpas
from flight_plans.models import DailyWorkLog


class RpasMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rpas
        fields = ("id", "cor_number", "rpas_serial")


class DailyWorkLogForStatsSerializer(serializers.ModelSerializer):
    user_first_name = serializers.SerializerMethodField()

    def get_user_first_name(self, instance):
        if instance.user:
            return str(instance.user.first_name)
        return None

    class Meta:
        model = DailyWorkLog
        fields = (
            "id",
            "user_first_name",
            "operation_date",
            "bags_spread",
            "acres_sprayed",
        )


class ProjectsListSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    bags_spread = serializers.FloatField(read_only=True)
    acres_sprayed = serializers.FloatField(read_only=True)
    unique_rpas_count = serializers.IntegerField(read_only=True)

    def get_client_name(self, instance):
        if instance.client:
            return str(instance.client.name)
        return None

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "client_name",
            "is_complete",
            "start_date",
            "end_date",
            "target_bags",
            "target_spray_acres",
            "bags_spread",
            "acres_sprayed",
            "unique_rpas_count",
        )


class ReserveAirspaceListSerializer(GeoFeatureModelSerializer):
    """A class to serialize locations as GeoJSON compatible data"""

    rpas = RpasMinimalSerializer(many=True, read_only=True)
    mission_type_display = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    start_datetime = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    user_phone_number = serializers.SerializerMethodField()

    user_profile_pic = serializers.SerializerMethodField()
    user_organization = serializers.SerializerMethodField()

    def get_mission_type_display(self, obj):
        return obj.get_mission_type_display()

    def get_area(self, obj):
        return obj.get_area()

    def get_start_datetime(self, obj):
        return obj.get_start_datetime()

    def get_user_full_name(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.created_by:
            return str(instance.created_by.get_full_name())
        else:
            return None

    def get_user_phone_number(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.created_by:
            return str(instance.get_phone_number)
        else:
            return None

    def get_user_organization(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.created_by:
            return str(instance.get_organization)
        else:
            return None

    def get_user_profile_pic(self, instance):

        request = self.context.get("request")
        # print(instance, "should be userprofile instance")
        if instance.created_by.userprofile.profile_pic:
            return request.build_absolute_uri(instance.get_user_profile_pic)
        else:
            return None

    class Meta:
        model = ReserveAirspace
        geo_field = "geom"
        fields = (
            "id",
            "user_full_name",
            "user_phone_number",
            "user_profile_pic",
            "user_organization",
            "created_by",
            "rpas",
            "start_day",
            "start_time",
            "start_datetime",
            "end",
            "mission_type_display",
            "area",
            "application_number",
            "status",
            "expiry",
            "centroid",
            "geom",
        )


class ReserveAirspaceDetailSerializer(GeoFeatureModelSerializer):
    """A class to serialize locations as GeoJSON compatible data"""

    rpas = RpasMinimalSerializer(many=True, read_only=True)
    mission_type_display = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    start_datetime = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    user_phone_number = serializers.SerializerMethodField()

    user_profile_pic = serializers.SerializerMethodField()
    user_organization = serializers.SerializerMethodField()

    def get_mission_type_display(self, obj):
        return obj.get_mission_type_display()

    def get_area(self, obj):
        return obj.get_area()

    def get_start_datetime(self, obj):
        return obj.get_start_datetime()

    def get_user_full_name(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.created_by:
            return str(instance.created_by.get_full_name())
        else:
            return None

    def get_user_phone_number(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.created_by:
            return str(instance.get_phone_number)
        else:
            return None

    def get_user_organization(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.created_by:
            return str(instance.get_organization)
        else:
            return None

    def get_user_profile_pic(self, instance):

        request = self.context.get("request")
        # print(instance, "should be userprofile instance")
        if instance.created_by.userprofile.profile_pic:
            return request.build_absolute_uri(instance.get_user_profile_pic)
        else:
            return None

    class Meta:
        model = ReserveAirspace

        geo_field = "geom"
        fields = (
            "id",
            "user_full_name",
            "user_phone_number",
            "user_profile_pic",
            "user_organization",
            "created_by",
            "rpas",
            "start_day",
            "start_time",
            "start_datetime",
            "end",
            "mission_type_display",
            "area",
            "application_number",
            "status",
            "expiry",
            "centroid",
            "geom",
        )
