from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

from mixer.backend.django import mixer

import pytest

pytestmark = pytest.mark.django_db

from applications.models import LogsUpload


@pytest.mark.django_db
class TestLogsUpload(TestCase):
    def test_userprofile_saves(self):

        log = mixer.blend(LogsUpload)

        assert LogsUpload.objects.count() == 1

