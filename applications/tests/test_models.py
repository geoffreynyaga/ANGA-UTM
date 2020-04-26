# import random
# import string

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

User = get_user_model()

from mixer.backend.django import mixer

import pytest


from applications.models import LogsUpload, ReserveAirspace
from rpas.models import Rpas, RpasModel, RpasModelType
from organizations.models import Organization, OrganizationDetails
from accounts.models import UserProfile


# def randomString(stringLength=20):
#     """Generate a random string of fixed length """
#     letters = string.ascii_lowercase
#     return "".join(random.choice(letters) for i in range(stringLength))


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestLogsUpload(TestCase):
    def test_userprofile_saves(self):

        log = mixer.blend(LogsUpload)

        assert LogsUpload.objects.count() == 1


class TestReserveAirspace(TestCase):
    def setUp(self):
        self.organization_details = mixer.blend(
            OrganizationDetails, name="organization_details_name"
        )

        self.organization = mixer.blend(
            Organization,
            organization_details=self.organization_details,
            organization_type="ROC",
        )

        print(self.organization, "self.organization")

        self.rpas_model_type = mixer.blend(RpasModelType, airframe_type="QUAD")
        self.my_rpas_model = mixer.blend(
            RpasModel,
            model_name="test_model_name",
            rpas_model_type=self.rpas_model_type,
        )
        print(self.my_rpas_model, "self.my_rpas_model")

        self.my_rpas = mixer.blend(
            Rpas, rpas_model=self.my_rpas_model, organization=self.organization,
        )

        print(self.my_rpas, "self.my_rpas")
        print(self.my_rpas.rpas_serial, "self.my_rpas.rpas_serial")

        self.my_user = mixer.blend(User, first_name="Geoffrey", last_name="Nyaga")
        print(self.my_user, "self.my_user")

        # URGENT: This means that user must be assigned to an organization before he/she can create reserve airspace

        self.my_user.userprofile.organization = self.organization
        self.my_user.userprofile.phone_number = "+254720000000"

        self.my_user.save()

    def test_reserve_airspace_saves(self):

        reserve = mixer.blend(
            ReserveAirspace, rpas=self.my_rpas, created_by=self.my_user
        )

        assert ReserveAirspace.objects.count() == 1

    def test_reserve_airspace_str_return(self):

        reserve = mixer.blend(
            ReserveAirspace, pk=1, rpas=self.my_rpas, created_by=self.my_user
        )
        reserve.save()
        assert str(ReserveAirspace.objects.get(pk=1)) == "FP/CAA/ROC/1"

    def test_reserve_airspace_get_rpas_method(self):

        reserve = mixer.blend(
            ReserveAirspace, pk=1, rpas=self.my_rpas, created_by=self.my_user
        )

        assert ReserveAirspace.objects.last().get_rpas == "test_model_name"

    def test_reserve_airspace_get_name_method(self):

        reserve = mixer.blend(
            ReserveAirspace, pk=1, rpas=self.my_rpas, created_by=self.my_user
        )

        assert ReserveAirspace.objects.last().get_name == "Geoffrey Nyaga"

    def test_reserve_airspace_get_phone_number_method(self):
        non_organizational_user_profile = UserProfile.objects.last()
        non_organizational_user_profile.phone_number = "+254720000000"
        non_organizational_user_profile.save()

        reserve = mixer.blend(
            ReserveAirspace, pk=1, rpas=self.my_rpas, created_by=self.my_user
        )

        assert ReserveAirspace.objects.last().get_phone_number == "+254720000000"

    def test_reserve_airspace_get_organization_method(self):

        non_organizational_user_profile = UserProfile.objects.last()
        non_organizational_user_profile.organization = self.organization
        non_organizational_user_profile.save()

        reserve = mixer.blend(
            ReserveAirspace, pk=1, rpas=self.my_rpas, created_by=self.my_user
        )

        assert (
            ReserveAirspace.objects.last().get_organization
            == "organization_details_name"
        )

    def test_reserve_airspace_get_airframe_type_method(self):

        reserve = mixer.blend(
            ReserveAirspace, pk=1, rpas=self.my_rpas, created_by=self.my_user
        )

        assert ReserveAirspace.objects.last().get_airframe_type == "QUADCOPTER"

    def test_reserve_airspace_fails_with_no_organization_in_user_profile(self):
        """ This test is supposed to test whether a validation error is raised when someone with no attached orhganisation tries to reserve airspace
        """

        my_user = mixer.blend(User, first_name="Geoffrey", last_name="Nyaga")

        # with self.assertRaises(AttributeError):
        #     x = mixer.blend(
        #         ReserveAirspace,
        #         pk=1,
        #         rpas=self.my_rpas,
        #         created_by=my_user,
        #     )

        #     x.full_clean()

        with pytest.raises(Exception):

            x = mixer.blend(
                ReserveAirspace, pk=1, rpas=self.my_rpas, created_by=my_user,
            )

            assert x.full_clean()
