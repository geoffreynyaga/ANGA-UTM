from rpas.models import Rpas
from django.contrib.auth.models import User
from rest_framework import serializers

from flight_plans.models import FlightLog
from organizations.models import Organization, OrganizationDetails
from accounts.models import UserProfile
from applications.models import ReserveAirspace


class UserProfileUASListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rpas
        fields = (
            "id",
            "rpas_serial",
            "rpas_nickname",
        )


class UserProfileFlightLogSerializer(serializers.ModelSerializer):
    date_created = serializers.SerializerMethodField()

    def get_date_created(self, instance):

        if instance.date_created:
            from django.contrib.humanize.templatetags.humanize import naturalday

            natural_day = naturalday(instance.date_created)
            return natural_day
        else:
            return None

    class Meta:
        model = ReserveAirspace
        fields = (
            "id",
            "date_created",
            "application_number",
        )


class OrganizationDetailsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, instance):
        request = self.context.get("request")
        # print(instance, "should be userprofile instance")
        if instance.logo:
            return request.build_absolute_uri(instance.get_logo_url())
            # return None
        else:
            return None

    class Meta:
        model = OrganizationDetails
        fields = (
            "name",
            "city",
            "website",
            "logo",
        )


class UserProfileOrganizationSerializer(serializers.ModelSerializer):
    organization_details = OrganizationDetailsSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = (
            "organization_details",
            "caa_no",
        )


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    userprofile.profile_pic.url
    userprofile.phone_number
    userprofile.bio
    userprofile.location
    userprofile.birth_date

    userprofile.user.get_full_name
    userprofile.user.username

    userprofile.organization.organization_details.name 
    userprofile.organization (roc number)
    userprofile.organization.organization_details.city
    userprofile.organization.organization_details.website

    thisuser = User.objects.get(pk=pk)
    org = thisuser.userprofile.organization
    context["myrpas"] = Rpas.objects.filter(organization=org)
    context["myflightlogs"] = FlightLog.objects.filter(user=thisuser)

    myflightlog.pk
    myflightlog.reserve_airspace.application_number

    rpas.rpas_serial
    rpas.pk

    """

    full_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    profile_pic = serializers.SerializerMethodField()
    organization = UserProfileOrganizationSerializer(read_only=True)

    def get_profile_pic(self, instance):
        request = self.context.get("request")
        # print(instance, "should be userprofile instance")
        if instance.profile_pic:
            return request.build_absolute_uri(instance.get_userprofile_pic_url())
            # return None
        else:
            return None

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = UserProfile
        fields = (
            "full_name",
            "username",
            "phone_number",
            "bio",
            "location",
            "birth_date",
            "profile_pic",
            "organization",
        )

