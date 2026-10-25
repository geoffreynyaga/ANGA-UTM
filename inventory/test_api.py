from django.urls import reverse
from rest_framework.test import APIClient

from inventory.models import (
    ComponentRequest,
    ComponentType,
    ComponentUnit,
    StockLot,
)
from inventory.tests import InventoryTestData, make_organization, make_user


class InventoryAPITestCase(InventoryTestData):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(self.pilot)


class CurrentUserAPITests(InventoryAPITestCase):
    def test_reports_approval_rights(self):
        pilot = self.client.get(reverse("inventory_me_api")).data
        self.client.force_authenticate(self.manager)
        manager = self.client.get(reverse("inventory_me_api")).data

        self.assertFalse(pilot["can_approve"])
        self.assertTrue(manager["can_approve"])


class ComponentListAPITests(InventoryAPITestCase):
    def test_list_returns_stock_for_own_organization(self):
        StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=7,
            created_by=self.pilot,
        )
        other = make_organization("Other")
        StockLot.add(
            organization=other,
            component_type=self.propeller,
            quantity=50,
            created_by=self.pilot,
        )

        response = self.client.get(reverse("inventory_components_api"))

        self.assertEqual(response.status_code, 200)
        propeller = next(c for c in response.data if c["id"] == self.propeller.pk)
        self.assertEqual(propeller["available"], 7)
        self.assertTrue(propeller["has_stock_history"])

    def test_proposed_types_are_pending(self):
        response = self.client.post(
            reverse("inventory_components_api"),
            {"name": "Generator Fuel Filter", "tags": ["Gen", "filter"]},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        component_type = ComponentType.objects.get(pk=response.data["id"])
        self.assertEqual(component_type.status, ComponentType.PENDING)
        self.assertEqual(component_type.proposed_by, self.pilot)
        self.assertEqual(sorted(response.data["tags"]), ["filter", "gen"])

    def test_blank_part_numbers_do_not_clash(self):
        url = reverse("inventory_components_api")
        first = self.client.post(url, {"name": "A", "part_number": ""}, format="json")
        second = self.client.post(url, {"name": "B", "part_number": ""}, format="json")

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertIsNone(second.data["part_number"])

    def test_organization_users_can_only_change_tags(self):
        response = self.client.patch(
            reverse("inventory_component_detail_api", args=[self.propeller.pk]),
            {"name": "Renamed", "tags": ["prop"]},
            format="json",
        )

        self.propeller.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.propeller.name, "Propeller CW")
        self.assertEqual(response.data["tags"], ["prop"])

    def test_caa_users_cannot_write(self):
        caa = make_user("caa@example.com", self.organization, role="caa")
        self.client.force_authenticate(caa)

        response = self.client.post(
            reverse("inventory_components_api"), {"name": "X"}, format="json"
        )

        self.assertEqual(response.status_code, 403)


class AddStockAPITests(InventoryAPITestCase):
    def test_add_quantity_to_lot(self):
        url = reverse("inventory_add_stock_api")
        self.client.post(
            url, {"component_type": self.propeller.pk, "quantity": 3}, format="json"
        )
        response = self.client.post(
            url, {"component_type": self.propeller.pk, "quantity": 2}, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["lot"]["quantity"], 5)

    def test_add_serialized_units(self):
        response = self.client.post(
            reverse("inventory_add_stock_api"),
            {"component_type": self.battery.pk, "serial_numbers": ["B1", "B2"]},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ComponentUnit.objects.count(), 2)

    def test_duplicate_serial_is_rejected(self):
        ComponentUnit.objects.create(
            organization=self.organization,
            component_type=self.battery,
            serial_number="B1",
        )

        response = self.client.post(
            reverse("inventory_add_stock_api"),
            {"component_type": self.battery.pk, "serial_numbers": ["B1"]},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("serial_numbers", response.data)

    def test_unit_can_be_scrapped_but_not_installed(self):
        unit = ComponentUnit.objects.create(
            organization=self.organization,
            component_type=self.battery,
            serial_number="B1",
        )
        url = reverse("inventory_unit_api", args=[unit.pk])

        installed = self.client.patch(url, {"lifecycle": "installed"}, format="json")
        scrapped = self.client.patch(
            url, {"lifecycle": "scrapped", "serviceable": False}, format="json"
        )

        self.assertEqual(installed.status_code, 400)
        self.assertEqual(scrapped.status_code, 200)


class ComponentRequestAPITests(InventoryAPITestCase):
    def setUp(self):
        super().setUp()
        self.lot = StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=5,
            created_by=self.manager,
        )

    def place(self, quantity=2):
        return self.client.post(
            reverse("inventory_requests_api"),
            {"rpas": self.rpas.pk, "lot": self.lot.pk, "quantity": quantity},
            format="json",
        )

    def test_request_and_approve(self):
        response = self.place()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "pending")

        self.client.force_authenticate(self.manager)
        approve = self.client.post(
            reverse("inventory_request_action_api", args=[response.data["id"], "approve"])
        )

        self.assertEqual(approve.status_code, 200)
        self.assertEqual(approve.data["status"], "approved")

    def test_over_request_returns_400(self):
        response = self.place(quantity=9)

        self.assertEqual(response.status_code, 400)

    def test_pilot_approval_returns_400(self):
        request_id = self.place().data["id"]

        response = self.client.post(
            reverse("inventory_request_action_api", args=[request_id, "approve"])
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            ComponentRequest.objects.get(pk=request_id).status, ComponentRequest.PENDING
        )

    def test_other_organizations_cannot_see_requests(self):
        self.place()
        outsider = make_user("out@example.com", make_organization("Other"))
        self.client.force_authenticate(outsider)

        response = self.client.get(reverse("inventory_requests_api"))

        self.assertEqual(response.data, [])
