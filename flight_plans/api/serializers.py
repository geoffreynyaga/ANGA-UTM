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
        return obj.get_mission_type_display()

    class Meta:
        model = ReserveAirspace
        fields = (
            "rpas_name",
            "start_day",
            "start_time",
            "end",
            "created_by",
            "mission_type",
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

    ==============================================

    full_name = serializers.SerializerMethodField()

    user_profile_pic_thumbnail = serializers.SerializerMethodField()

    total_contributed = serializers.SerializerMethodField()

    def get_total_contributed(self, obj):
        all_transactions = (
            ClientToPaybill.objects.filter(
                receiver__pk=self.context.get("group_pk"), sender=obj
            )
            .filter(is_verified=True)
            .aggregate(Sum("amount"))
        )

        # print(all_transactions, "all transactions for user", obj)

        return all_transactions["amount__sum"]

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_user_profile_pic_thumbnail(self, instance):
        request = self.context.get("request")

        if instance.userprofile.profile_pic_thumbnail:
            return request.build_absolute_uri(
                instance.userprofile.get_user_profile_pic_thumbnail()
            )
        else:
            return None


    """

    user_first_name = serializers.SerializerMethodField()
    user_last_name = serializers.SerializerMethodField()
    reserve_airspace = FlightLogReserveAirspaceSerializer(read_only=True)

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

    class Meta:
        model = FlightLog
        fields = (
            "user_first_name",
            "user_last_name",
            "reserve_airspace",
            "emmergency_info",
            "pre_flight",
            "post_flight",
        )

