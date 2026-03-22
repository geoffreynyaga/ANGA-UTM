from django.contrib.auth import get_user_model
from django.test import TestCase

from flight_plans.models import DailyWorkLog

# Create your tests here.


class DailyWorkLogModelTests(TestCase):
	def test_str_handles_missing_reserve_airspace(self):
		user_model = get_user_model()
		user = user_model.objects.create_user(
			username="flightlog-test-user",
			email="flightlog-test@example.com",
			password="safe-password-123",
		)
		flight_log = DailyWorkLog.objects.create(user=user, reserve_airspace=None)

		self.assertEqual(str(flight_log), f"DailyWorkLog #{flight_log.pk}")
