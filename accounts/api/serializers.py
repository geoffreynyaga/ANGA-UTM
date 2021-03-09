from rpas.models import Rpas
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers, exceptions


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


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        print(data, "this is data")

        """
        # print(data, "this is data")
       OrderedDict([('username', 'geoff'), ('password', 'password')]) this is data
        """
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    data["user"] = user

                else:
                    msg = "user is deactivated"
                    raise exceptions.ValidationError(msg)

            else:
                msg = "Unable to login with the given username and password"
                data["err1"] = msg
                raise exceptions.ValidationError(msg)

        else:
            msg = "You must provide both Username and Password"
            data["err1"] = msg
            raise exceptions.ValidationError(msg)

        return data


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    # def validate_phone_number(self, value):

    #     phone_number = str(value)
    #     # str because it comes in a a PhoneNumberField class

    #     # URGENT : add phone number verification as well(safaricom)
    #     # No need to check e164 standard, serializer field already does that
    #     # FIXED:
    #     from mpesa.phone import phone_number_conversions

    #     try:
    #         x = phone_number_conversions.check_phone_number_carrier_name(phone_number)
    #         print(x, "should be saf")
    #         print(type(x), "should be saf")
    #         print(x == "Safaricom", "should be false")
    #         print(x != "Safaricom", "should be true")

    #         if x != "Safaricom":
    #             print(f"number is not safaricom but {x}")
    #             raise ValidationError(f"We do not accept {x} numbers, only Safaricom")
    #         else:
    #             print(f"number is  safaricom <> {x}")
    #             pass

    #     except:
    #         raise ValidationError(f"We do not accept {x} numbers, only Safaricom")

    #     user_qs = User.objects.filter(phone_number=phone_number)  # why not get?

    #     if user_qs.exists():
    #         # check if active. If Active return the error below else proceed to return phone_number
    #         if user_qs.count() > 1:
    #             raise ValidationError(
    #                 "Internal Error, kindly contact us to resolve this"
    #             )
    #         elif user_qs.count() == 1:
    #             print("sweet spot")
    #             user = user_qs[0]
    #             print(user, "should be the single user")
    #             if user.is_active == False:
    #                 print("user is registered but not confirmed")
    #                 return phone_number
    #             else:
    #                 raise ValidationError(
    #                     "This phone number has already been registered."
    #                 )
    #         else:
    #             print("user count is zero")
    #             return phone_number
    #     else:
    #         return phone_number
