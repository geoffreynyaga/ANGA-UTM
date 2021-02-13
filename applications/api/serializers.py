from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeoModelSerializer
from applications.models import ReserveAirspace


class ReserveAirspaceListSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    rpas_name = serializers.SerializerMethodField()
    mission_type_display = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    start_datetime = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    user_phone_number = serializers.SerializerMethodField()

    rpas_serial = serializers.SerializerMethodField()
    rpas_pic = serializers.SerializerMethodField()
    airframe_type = serializers.SerializerMethodField()
    user_profile_pic = serializers.SerializerMethodField()
    user_organization = serializers.SerializerMethodField()

    def get_rpas_name(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.rpas:
            return str(instance.rpas.rpas_nickname)
        else:
            return None

    def get_rpas_serial(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.rpas:
            return str(instance.rpas.rpas_serial)
        else:
            return None

    def get_rpas_pic(self, instance):

        request = self.context.get("request")
        # print(instance, "should be userprofile instance")
        if instance.rpas.rpas_pic:
            return request.build_absolute_uri(instance.get_rpas_pic)
            # return None
        else:
            return None

    def get_airframe_type(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.rpas:
            return str(instance.get_airframe_type)
        else:
            return None

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
            "rpas_name",
            "rpas_serial",
            "rpas_pic",
            "airframe_type",
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
    """ A class to serialize locations as GeoJSON compatible data """

    rpas_name = serializers.SerializerMethodField()
    mission_type_display = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    start_datetime = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    user_phone_number = serializers.SerializerMethodField()

    rpas_serial = serializers.SerializerMethodField()
    rpas_pic = serializers.SerializerMethodField()
    airframe_type = serializers.SerializerMethodField()
    user_profile_pic = serializers.SerializerMethodField()
    user_organization = serializers.SerializerMethodField()

    def get_rpas_name(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.rpas:
            return str(instance.rpas.rpas_nickname)
        else:
            return None

    def get_rpas_serial(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.rpas:
            return str(instance.rpas.rpas_serial)
        else:
            return None

    def get_rpas_pic(self, instance):

        request = self.context.get("request")
        # print(instance, "should be userprofile instance")
        if instance.rpas.rpas_pic:
            return request.build_absolute_uri(instance.get_rpas_pic)
            # return None
        else:
            return None

    def get_airframe_type(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.rpas:
            return str(instance.get_airframe_type)
        else:
            return None

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
            "rpas_name",
            "rpas_serial",
            "rpas_pic",
            "airframe_type",
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
