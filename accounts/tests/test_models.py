from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

from mixer.backend.django import mixer

import pytest

pytestmark = pytest.mark.django_db

from accounts.models import UserProfile


@pytest.mark.django_db
class TestUserProfile(TestCase):
    def test_userprofile_saves(self):

        user = mixer.blend(User, username="geoffrey")

        assert UserProfile.objects.count() == 1

    def test_userprofile_return_str(self):

        user = mixer.blend(User, username="nyaga")

        assert str(UserProfile.objects.last()) == "nyaga"
