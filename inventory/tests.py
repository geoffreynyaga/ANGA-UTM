from io import StringIO

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import UserProfile
from organizations.models import Organization, OrganizationDetails
from rpas.models import Rpas

from inventory.models import (
    ComponentRequest,
    ComponentType,
    ComponentUnit,
    StockLot,
    Tag,
)


def make_organization(name):
    details = OrganizationDetails.objects.create(
        name=name, city="Nairobi", website="https://example.com"
    )
    organization = Organization(
        organization_details=details, organization_type="ROC", caa_no=f"TEMP-{name}"
    )
    organization.save()
    return organization


def make_user(email, organization, role="pilot"):
    user = get_user_model().objects.create_user(
        email=email, password="safe-password-123", role=role
    )
    UserProfile.objects.update_or_create(
        user_id=user.pk, defaults={"organization": organization}
    )
    user.refresh_from_db()
    return user


def make_rpas(user, serial):
    return Rpas.objects.create(
        user=user, organization=user.userprofile.organization, rpas_serial=serial
    )


class InventoryTestData(TestCase):
    def setUp(self):
        self.organization = make_organization("Skybound")
        self.pilot = make_user("pilot@example.com", self.organization)
        self.manager = make_user(
            "ops@example.com", self.organization, role="ops_manager"
        )
        self.rpas = make_rpas(self.pilot, "T50-0001")
        self.propeller = ComponentType.objects.create(name="Propeller CW")
        self.battery = ComponentType.objects.create(
            name="DB1560 Battery", is_serialized=True
        )


class StockLotTests(InventoryTestData):
    def test_adding_same_part_increments_existing_lot(self):
        StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=4,
            created_by=self.pilot,
        )
        lot = StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=6,
            created_by=self.pilot,
        )

        self.assertEqual(StockLot.objects.count(), 1)
        self.assertEqual(lot.quantity, 10)

    def test_used_parts_get_their_own_lot(self):
        StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=4,
            created_by=self.pilot,
        )
        StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=2,
            created_by=self.pilot,
            condition=StockLot.USED,
            origin=StockLot.SALVAGED,
            source_rpas=self.rpas,
        )

        self.assertEqual(StockLot.objects.count(), 2)

    def test_serialized_types_cannot_be_added_as_lots(self):
        with self.assertRaises(ValidationError):
            StockLot.add(
                organization=self.organization,
                component_type=self.battery,
                quantity=1,
                created_by=self.pilot,
            )


class StockAnnotationTests(InventoryTestData):
    def test_with_stock_counts_lots_and_available_units(self):
        StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=3,
            created_by=self.pilot,
        )
        ComponentUnit.objects.create(
            organization=self.organization,
            component_type=self.battery,
            serial_number="B1",
        )
        ComponentUnit.objects.create(
            organization=self.organization,
            component_type=self.battery,
            serial_number="B2",
            lifecycle=ComponentUnit.INSTALLED,
        )
        other = make_organization("Other")
        ComponentUnit.objects.create(
            organization=other, component_type=self.battery, serial_number="B3"
        )

        types = {t.pk: t for t in ComponentType.objects.with_stock(self.organization)}

        self.assertEqual(types[self.propeller.pk].available, 3)
        self.assertEqual(types[self.battery.pk].available, 1)

    def test_out_of_stock_types_keep_their_history(self):
        lot = StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=1,
            created_by=self.pilot,
        )
        ComponentRequest.place(requested_by=self.pilot, rpas=self.rpas, lot=lot)
        never_stocked = ComponentType.objects.create(name="Spray Nozzle")

        types = {t.pk: t for t in ComponentType.objects.with_stock(self.organization)}

        self.assertEqual(types[self.propeller.pk].available, 0)
        self.assertTrue(types[self.propeller.pk].has_stock_history)
        self.assertFalse(types[never_stocked.pk].has_stock_history)


class ComponentRequestTests(InventoryTestData):
    def setUp(self):
        super().setUp()
        self.lot = StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=5,
            created_by=self.manager,
        )
        self.unit = ComponentUnit.objects.create(
            organization=self.organization,
            component_type=self.battery,
            serial_number="B1",
        )

    def test_placing_a_request_holds_lot_stock(self):
        request = ComponentRequest.place(
            requested_by=self.pilot, rpas=self.rpas, lot=self.lot, quantity=2
        )

        self.lot.refresh_from_db()
        self.assertEqual(self.lot.quantity, 3)
        self.assertEqual(request.status, ComponentRequest.PENDING)

    def test_cannot_request_more_than_in_stock(self):
        with self.assertRaises(ValidationError):
            ComponentRequest.place(
                requested_by=self.pilot, rpas=self.rpas, lot=self.lot, quantity=6
            )

    def test_reserved_unit_cannot_be_requested_twice(self):
        ComponentRequest.place(requested_by=self.pilot, rpas=self.rpas, unit=self.unit)

        with self.assertRaises(ValidationError):
            ComponentRequest.place(
                requested_by=self.manager, rpas=self.rpas, unit=self.unit
            )

    def test_cannot_request_for_another_organizations_drone(self):
        other = make_organization("Other")
        outsider = make_user("out@example.com", other)
        other_rpas = make_rpas(outsider, "M300-1")

        with self.assertRaises(ValidationError):
            ComponentRequest.place(
                requested_by=self.pilot, rpas=other_rpas, lot=self.lot
            )

    def test_approval_issues_the_unit(self):
        request = ComponentRequest.place(
            requested_by=self.pilot, rpas=self.rpas, unit=self.unit
        )

        request.approve(self.manager)

        self.unit.refresh_from_db()
        self.assertEqual(request.status, ComponentRequest.APPROVED)
        self.assertEqual(self.unit.lifecycle, ComponentUnit.ISSUED)

    def test_pilot_cannot_approve(self):
        request = ComponentRequest.place(
            requested_by=self.manager, rpas=self.rpas, lot=self.lot
        )

        with self.assertRaises(ValidationError):
            request.approve(self.pilot)

    def test_approver_cannot_approve_own_request(self):
        request = ComponentRequest.place(
            requested_by=self.manager, rpas=self.rpas, lot=self.lot
        )

        with self.assertRaises(ValidationError):
            request.approve(self.manager)

    def test_staff_can_approve(self):
        self.pilot.is_staff = True
        self.pilot.save()
        request = ComponentRequest.place(
            requested_by=self.manager, rpas=self.rpas, lot=self.lot
        )

        request.approve(self.pilot)

        self.assertEqual(request.status, ComponentRequest.APPROVED)

    def test_rejection_returns_stock(self):
        lot_request = ComponentRequest.place(
            requested_by=self.pilot, rpas=self.rpas, lot=self.lot, quantity=2
        )
        unit_request = ComponentRequest.place(
            requested_by=self.pilot, rpas=self.rpas, unit=self.unit
        )

        lot_request.reject(self.manager)
        unit_request.reject(self.manager)

        self.lot.refresh_from_db()
        self.unit.refresh_from_db()
        self.assertEqual(self.lot.quantity, 5)
        self.assertEqual(self.unit.lifecycle, ComponentUnit.AVAILABLE)

    def test_cancel_only_by_requester(self):
        request = ComponentRequest.place(
            requested_by=self.pilot, rpas=self.rpas, lot=self.lot
        )

        with self.assertRaises(ValidationError):
            request.cancel(self.manager)
        request.cancel(self.pilot)

        self.assertEqual(request.status, ComponentRequest.CANCELLED)

    def test_decided_requests_cannot_change(self):
        request = ComponentRequest.place(
            requested_by=self.pilot, rpas=self.rpas, lot=self.lot
        )
        request.approve(self.manager)

        with self.assertRaises(ValidationError):
            request.reject(self.manager)


class MergeTests(InventoryTestData):
    def test_merge_moves_stock_requests_and_tags(self):
        duplicate = ComponentType.objects.create(
            name="Prop CW", status=ComponentType.PENDING
        )
        duplicate.tags.add(Tag.objects.create(name="Prop"))
        StockLot.add(
            organization=self.organization,
            component_type=self.propeller,
            quantity=2,
            created_by=self.pilot,
        )
        duplicate_lot = StockLot.add(
            organization=self.organization,
            component_type=duplicate,
            quantity=3,
            created_by=self.pilot,
        )
        request = ComponentRequest.place(
            requested_by=self.pilot, rpas=self.rpas, lot=duplicate_lot
        )

        duplicate.merge_into(self.propeller)

        request.refresh_from_db()
        self.assertFalse(ComponentType.objects.filter(pk=duplicate.pk).exists())
        self.assertEqual(self.propeller.stock_lots.get().quantity, 4)
        self.assertEqual(request.component_type, self.propeller)
        self.assertEqual(request.lot.component_type, self.propeller)
        self.assertEqual(list(self.propeller.tags.values_list("name", flat=True)), ["prop"])


class ImportCatalogTests(TestCase):
    def test_import_is_repeatable(self):
        from django.core.management import call_command

        call_command("import_component_catalog", stdout=StringIO())
        call_command("import_component_catalog", stdout=StringIO())

        part = ComponentType.objects.get(part_number="YC.JG.MY001043")
        self.assertEqual(part.diagram_name, "Front Cover of Front Shell")
        self.assertEqual(part.aircraft_models.get().name, "Agras T50")
        self.assertEqual(ComponentType.objects.count(), 245)
