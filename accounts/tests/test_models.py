from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

from accounts.models import UserProfile


@pytest.mark.django_db
class TestUserProfile(TestCase):
    def test_userprofile_saves(self):
        user = mixer.blend(User, email="geoffrey")

        assert UserProfile.objects.count() == 1

    def test_userprofile_return_str(self):
        user = mixer.blend(User, email="nyaga")

        assert str(UserProfile.objects.last()) == "nyaga"
