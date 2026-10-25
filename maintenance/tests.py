import datetime

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient

from inventory.models import ComponentRequest, ComponentUnit, StockLot
from inventory.tests import InventoryTestData, make_rpas
from maintenance.models import MaintenanceRecord


class MaintenanceTestData(InventoryTestData):
    def setUp(self):
        super().setUp()
        self.unit = ComponentUnit.objects.create(
            organization=self.organization,
            component_type=self.battery,
            serial_number="B1",
        )
        self.lot = StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=4,
            created_by=self.manager,
        )
        self.unit_request = ComponentRequest.place(
            requested_by=self.pilot, rpas=self.rpas, unit=self.unit
        )
        self.unit_request.approve(self.manager)
        self.lot_request = ComponentRequest.place(
            requested_by=self.pilot, rpas=self.rpas, lot=self.lot, quantity=2
        )
        self.lot_request.approve(self.manager)

    def record(self, **kwargs):
        defaults = {
            "performed_by": self.pilot,
            "rpas": self.rpas,
            "date_performed": datetime.date(2026, 10, 1),
            "description": "Replaced battery and propellers",
        }
        return MaintenanceRecord.record(**{**defaults, **kwargs})


class MaintenanceRecordTests(MaintenanceTestData):
    def test_fitted_components_are_installed_on_the_drone(self):
        self.record(component_requests=[self.unit_request, self.lot_request])

        self.unit.refresh_from_db()
        self.lot_request.refresh_from_db()
        self.assertEqual(self.unit.lifecycle, ComponentUnit.INSTALLED)
        self.assertEqual(self.unit.rpas, self.rpas)
        self.assertEqual(self.lot_request.status, ComponentRequest.INSTALLED)

    def test_pending_requests_cannot_be_fitted(self):
        pending = ComponentRequest.place(
            requested_by=self.pilot, rpas=self.rpas, lot=self.lot
        )

        with self.assertRaises(ValidationError):
            self.record(component_requests=[pending])

    def test_requests_for_another_drone_cannot_be_fitted(self):
        other_rpas = make_rpas(self.pilot, "T50-0002")

        with self.assertRaises(ValidationError):
            self.record(rpas=other_rpas, component_requests=[self.lot_request])

    def test_installed_requests_cannot_be_fitted_twice(self):
        self.record(component_requests=[self.lot_request])
        self.lot_request.refresh_from_db()

        with self.assertRaises(ValidationError):
            self.record(component_requests=[self.lot_request])

    def test_serviced_units_get_the_latest_service_date(self):
        battery = ComponentUnit.objects.create(
            organization=self.organization,
            component_type=self.battery,
            serial_number="B2",
        )
        self.record(serviced_units=[battery], date_performed=datetime.date(2026, 10, 5))
        self.record(serviced_units=[battery], date_performed=datetime.date(2026, 9, 1))

        battery.refresh_from_db()
        self.assertEqual(battery.last_serviced, datetime.date(2026, 10, 5))


class MaintenanceAPITests(MaintenanceTestData):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(self.pilot)

    def test_create_record_with_pdf_report(self):
        report = SimpleUploadedFile(
            "report.pdf", b"%PDF-1.4 test", content_type="application/pdf"
        )

        response = self.client.post(
            reverse("maintenance_records_api"),
            {
                "rpas": self.rpas.pk,
                "date_performed": "2026-10-01",
                "service_type": "repair",
                "description": "Swapped battery",
                "component_requests": [self.unit_request.pk],
                "report": report,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["components_used"][0]["serial_number"], "B1")
        self.assertEqual(response.data["performed_by"], self.pilot.pk)

    def test_non_pdf_report_is_rejected(self):
        report = SimpleUploadedFile("report.docx", b"x")

        response = self.client.post(
            reverse("maintenance_records_api"),
            {
                "rpas": self.rpas.pk,
                "date_performed": "2026-10-01",
                "description": "Swapped battery",
                "report": report,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("report", response.data)

    def test_drone_list_shows_last_serviced(self):
        self.record(date_performed=datetime.date(2026, 10, 3))

        response = self.client.get(reverse("maintenance_rpas_api"))

        self.assertEqual(response.data[0]["last_serviced"], "2026-10-03")
        self.assertEqual(response.data[0]["record_count"], 1)

    def test_installable_requests_lists_approved_requests_for_drone(self):
        response = self.client.get(
            reverse("maintenance_installable_requests_api"), {"rpas": self.rpas.pk}
        )

        self.assertEqual(
            {r["id"] for r in response.data},
            {self.unit_request.pk, self.lot_request.pk},
        )
