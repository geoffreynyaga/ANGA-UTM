from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import UserProfile
from organizations.models import Organization, OrganizationDetails


class AllCompanyFlightLogsTests(TestCase):
	def test_logs_page_uses_userprofile_organization_relation(self):
		user_model = get_user_model()
		organization_details = OrganizationDetails.objects.create(
			name="Skybound Ops",
			city="Nairobi",
			website="https://example.com",
		)
		organization = Organization(
			organization_details=organization_details,
			organization_type="ROC",
			caa_no="TEMP-ROC-1",
		)
		organization.save()
		user = user_model.objects.create_user(
			username="pilot-user",
			email="pilot@example.com",
			password="safe-password-123",
		)
		colleague = user_model.objects.create_user(
			username="observer-user",
			email="observer@example.com",
			password="safe-password-123",
		)
		UserProfile.objects.update_or_create(
			user_id=user.pk,
			defaults={"organization": organization},
		)
		UserProfile.objects.update_or_create(
			user_id=colleague.pk,
			defaults={"organization": organization},
		)

		self.client.force_login(user)

		response = self.client.get(reverse("all_company_flight_logs"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Skybound Ops")
		self.assertContains(response, "pilot@example.com")
		self.assertContains(response, "observer@example.com")
