from applications.models import ReserveAirspace
from rest_framework import serializers
from flight_plans.models import FlightLog


class FlightLogReserveAirspaceSerializer(serializers.ModelSerializer):
    rpas_name = serializers.SerializerMethodField()
    mission_type_display = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    start_datetime = serializers.SerializerMethodField()

    def get_rpas_name(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.rpas:
            return str(instance.rpas.rpas_nickname)
        else:
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
    """
    user.last_name
    user.first_name

    log.reserve_airspace.get_start_datetime
    log.reserve_airspace.application_number
    log.reserve_airspace.rpas
    log.reserve_airspace.get_mission_type_display
    log.reserve_airspace.get_area
    log.reserve_airspace.status

    log.pre_flight.no_of_flights
    log.get_post_flight_completion

    """

    user_first_name = serializers.SerializerMethodField()
    user_last_name = serializers.SerializerMethodField()
    reserve_airspace = FlightLogReserveAirspaceSerializer(read_only=True)
    no_of_flights = serializers.SerializerMethodField()
    post_flight_completion = serializers.SerializerMethodField()
    pre_flight_completion = serializers.SerializerMethodField()

    def get_user_first_name(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.user:
            return str(instance.user.first_name)
        else:
            return None

    def get_user_last_name(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.user:
            return str(instance.user.last_name)
        else:
            return None

    def get_no_of_flights(self, instance):

        # print(instance.created_by, "should be group instance")
        if instance.user:
            return instance.pre_flight.no_of_flights
        else:
            return None

    def get_post_flight_completion(self, obj):
        return obj.get_post_flight_completion()

    def get_pre_flight_completion(self, obj):
        return obj.get_pre_flight_completion()

    class Meta:
        model = FlightLog
        fields = (
            "user_first_name",
            "user_last_name",
            "reserve_airspace",
            "no_of_flights",
            "post_flight_completion",
            "pre_flight_completion",
        )

