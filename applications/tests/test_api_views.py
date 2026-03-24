from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.test import TestCase

from mixer.backend.django import mixer

from applications.api.views import ProjectListExtraDetailsAPIView
from applications.models import Client, Project
from organizations.models import Organization, OrganizationDetails


User = get_user_model()


class TestProjectListExtraDetailsAPIView(TestCase):
    def setUp(self):
        self.view = ProjectListExtraDetailsAPIView()
        self.created_by = mixer.blend(User, email="projects@example.com")
        self.request_user = SimpleNamespace(
            userprofile=SimpleNamespace(organization=None)
        )

    def _get_response(self):
        self.view.request = SimpleNamespace(user=self.request_user)
        return self.view.get()

    def test_returns_message_when_user_has_no_organization(self):
        response = self._get_response()

        assert response.status_code == 400
        assert response.data == {
            "ResultDesc": "User is not connected to an organization. Please reach out to the admin for addition to company projects.",
            "projects": [],
        }

    def test_returns_message_when_organization_has_no_projects(self):
        organization_details = mixer.blend(
            OrganizationDetails, name="No Projects Organization"
        )
        organization = mixer.blend(
            Organization,
            organization_details=organization_details,
            organization_type="ROC",
        )
        self.request_user.userprofile.organization = organization

        response = self._get_response()

        assert response.status_code == 200
        assert response.data == {
            "ResultDesc": "This organization has no projects started.",
            "projects": [],
        }

    def test_returns_projects_when_organization_has_projects(self):
        organization_details = mixer.blend(
            OrganizationDetails, name="Active Projects Organization"
        )
        organization = mixer.blend(
            Organization,
            organization_details=organization_details,
            organization_type="ROC",
        )
        self.request_user.userprofile.organization = organization

        client = mixer.blend(
            Client,
            name="Acme Client",
            created_by=self.created_by,
        )
        project = mixer.blend(
            Project,
            name="Project One",
            organization=organization,
            client=client,
            created_by=self.created_by,
        )

        response = self._get_response()
        payload = response.data

        assert response.status_code == 200
        assert len(payload["projects"]) == 1
        assert payload["projects"][0]["id"] == project.id
        assert payload["projects"][0]["name"] == project.name