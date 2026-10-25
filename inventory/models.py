from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Count, Exists, F, OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

APPROVER_ROLES = ("ops_manager", "acc_manager")
READ_ONLY_ROLES = ("caa", "mod")


def can_approve(user):
    return user.is_staff or user.role in APPROVER_ROLES


def is_read_only(user):
    return user.role in READ_ONLY_ROLES


class AircraftModel(models.Model):
    """Curated aircraft list used to tag which components fit which drones."""

    manufacturer = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("manufacturer", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("manufacturer", "name"), name="unique_aircraft_model"
            )
        ]

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ComponentTypeQuerySet(models.QuerySet):
    def with_stock(self, organization):
        """Annotate stock counts for one organization.

        has_stock_history is true once the organization has ever stocked the
        type, so it can be listed as out of stock when the count reaches 0.
        """

        def subquery_total(queryset, aggregate):
            total = (
                queryset.filter(component_type=OuterRef("pk"), organization=organization)
                .order_by()
                .values("component_type")
                .annotate(total=aggregate)
                .values("total")
            )
            return Coalesce(Subquery(total), 0)

        units = ComponentUnit.objects.all()
        return self.annotate(
            lot_quantity=subquery_total(StockLot.objects.all(), Sum("quantity")),
            available_units=subquery_total(
                units.filter(lifecycle=ComponentUnit.AVAILABLE), Count("pk")
            ),
            unserviceable_units=subquery_total(
                units.filter(serviceable=False).exclude(
                    lifecycle=ComponentUnit.SCRAPPED
                ),
                Count("pk"),
            ),
            has_stock_history=Exists(
                StockLot.objects.filter(
                    component_type=OuterRef("pk"), organization=organization
                )
            )
            | Exists(
                units.filter(component_type=OuterRef("pk"), organization=organization)
            ),
        ).annotate(available=F("lot_quantity") + F("available_units"))


class ComponentType(models.Model):
    """Shared catalog entry, e.g. "T50 Propeller (CW)" or "Spray Tank Assembly"."""

    APPROVED = "approved"
    PENDING = "pending"
    STATUS_CHOICES = ((APPROVED, "Approved"), (PENDING, "Pending review"))

    name = models.CharField(max_length=150)
    part_number = models.CharField(max_length=60, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/components", blank=True)
    diagram_name = models.CharField(
        max_length=100, blank=True, help_text="Parts diagram the item appears on"
    )
    diagram_number = models.CharField(
        max_length=10, blank=True, help_text="Callout number on the parts diagram"
    )
    aircraft_models = models.ManyToManyField(
        AircraftModel, blank=True, related_name="component_types"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="component_types")
    is_serialized = models.BooleanField(
        default=False, help_text="Tracked one by one with a serial number"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
        help_text="Assembly this component belongs to",
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=APPROVED)
    proposed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_created = models.DateTimeField(auto_now_add=True)

    objects = ComponentTypeQuerySet.as_manager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        if self.part_number:
            return f"{self.name} ({self.part_number})"
        return self.name

    @transaction.atomic
    def merge_into(self, target):
        """Move all stock and requests to target, then delete this duplicate."""
        if target.pk == self.pk:
            raise ValidationError("Cannot merge a component type into itself.")
        for lot in self.stock_lots.all():
            target_lot = StockLot.add(
                organization=lot.organization,
                component_type=target,
                quantity=lot.quantity,
                condition=lot.condition,
                origin=lot.origin,
                source_rpas=lot.source_rpas,
                created_by=lot.created_by,
            )
            lot.requests.update(lot=target_lot)
        self.units.update(component_type=target)
        self.requests.update(component_type=target)
        self.children.update(parent=target)
        target.tags.add(*self.tags.all())
        target.aircraft_models.add(*self.aircraft_models.all())
        self.delete()


class StockItemFields(models.Model):
    NEW = "new"
    USED = "used"
    CONDITION_CHOICES = ((NEW, "New"), (USED, "Used"))

    PURCHASED = "purchased"
    SALVAGED = "salvaged"
    ORIGIN_CHOICES = ((PURCHASED, "Purchased"), (SALVAGED, "Salvaged"))

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default=NEW)
    origin = models.CharField(max_length=10, choices=ORIGIN_CHOICES, default=PURCHASED)
    source_rpas = models.ForeignKey(
        "rpas.Rpas",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
        help_text="Drone the item was salvaged from",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class StockLot(StockItemFields):
    """A counted pile of identical non-serialized parts, e.g. 40 M3 screws."""

    component_type = models.ForeignKey(
        ComponentType, on_delete=models.CASCADE, related_name="stock_lots"
    )
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.component_type} ({self.condition})"

    @classmethod
    @transaction.atomic
    def add(cls, *, organization, component_type, quantity, created_by, **fields):
        """Add to the matching lot if one exists, so the same part is not listed twice."""
        if component_type.is_serialized:
            raise ValidationError("Serialized components are added as units.")
        if quantity < 1:
            raise ValidationError("Quantity must be at least 1.")
        lot, _ = cls.objects.select_for_update().get_or_create(
            organization=organization,
            component_type=component_type,
            condition=fields.get("condition", cls.NEW),
            origin=fields.get("origin", cls.PURCHASED),
            source_rpas=fields.get("source_rpas"),
            defaults={"created_by": created_by},
        )
        lot.quantity = models.F("quantity") + quantity
        lot.save(update_fields=["quantity"])
        lot.refresh_from_db()
        return lot


class ComponentUnit(StockItemFields):
    """One physical serialized item, e.g. a battery or an RC controller."""

    AVAILABLE = "available"
    RESERVED = "reserved"
    ISSUED = "issued"
    INSTALLED = "installed"
    SCRAPPED = "scrapped"
    LIFECYCLE_CHOICES = (
        (AVAILABLE, "Available"),
        (RESERVED, "Reserved"),
        (ISSUED, "Issued"),
        (INSTALLED, "Installed"),
        (SCRAPPED, "Scrapped"),
    )

    component_type = models.ForeignKey(
        ComponentType, on_delete=models.CASCADE, related_name="units"
    )
    serial_number = models.CharField(max_length=60)
    serviceable = models.BooleanField(default=True)
    lifecycle = models.CharField(
        max_length=10, choices=LIFECYCLE_CHOICES, default=AVAILABLE
    )
    rpas = models.ForeignKey(
        "rpas.Rpas",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="component_units",
        help_text="Drone the unit is installed on",
    )
    parent_unit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="child_units",
        help_text="Assembly unit this unit is fitted to",
    )
    last_serviced = models.DateField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "component_type", "serial_number"),
                name="unique_unit_serial_per_organization",
            )
        ]

    def __str__(self):
        return f"{self.component_type.name} #{self.serial_number}"


class ComponentRequest(models.Model):
    """A request to take stock for a drone. Stock is held while pending."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    INSTALLED = "installed"
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
        (CANCELLED, "Cancelled"),
        (INSTALLED, "Installed"),
    )

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    component_type = models.ForeignKey(
        ComponentType, on_delete=models.PROTECT, related_name="requests"
    )
    rpas = models.ForeignKey(
        "rpas.Rpas", on_delete=models.PROTECT, related_name="component_requests"
    )
    lot = models.ForeignKey(
        StockLot, on_delete=models.PROTECT, blank=True, null=True, related_name="requests"
    )
    unit = models.ForeignKey(
        ComponentUnit,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="requests",
    )
    quantity = models.PositiveIntegerField(default=1)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+"
    )
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    date_decided = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return f"{self.quantity} x {self.component_type.name} for {self.rpas}"

    @classmethod
    @transaction.atomic
    def place(cls, *, requested_by, rpas, quantity=1, lot=None, unit=None, note=""):
        """Create a pending request and hold the stock it asks for."""
        organization = requested_by.userprofile.organization
        if (lot is None) == (unit is None):
            raise ValidationError("Request either a stock lot or a unit.")
        if rpas.organization_id != organization.pk:
            raise ValidationError("The drone belongs to another organization.")

        if lot is not None:
            lot = StockLot.objects.select_for_update().get(pk=lot.pk)
            if lot.organization_id != organization.pk:
                raise ValidationError("The stock belongs to another organization.")
            if quantity < 1 or quantity > lot.quantity:
                raise ValidationError(f"Only {lot.quantity} in stock.")
            lot.quantity -= quantity
            lot.save(update_fields=["quantity"])
            component_type = lot.component_type
        else:
            unit = ComponentUnit.objects.select_for_update().get(pk=unit.pk)
            if unit.organization_id != organization.pk:
                raise ValidationError("The unit belongs to another organization.")
            if unit.lifecycle != ComponentUnit.AVAILABLE:
                raise ValidationError("This unit is not available.")
            unit.lifecycle = ComponentUnit.RESERVED
            unit.save(update_fields=["lifecycle"])
            component_type = unit.component_type
            quantity = 1

        return cls.objects.create(
            organization=organization,
            component_type=component_type,
            rpas=rpas,
            lot=lot,
            unit=unit,
            quantity=quantity,
            note=note,
            requested_by=requested_by,
        )

    def _decide(self, user, status):
        if self.status != self.PENDING:
            raise ValidationError("Only pending requests can be changed.")
        self.status = status
        self.decided_by = user
        self.date_decided = timezone.now()
        self.save(update_fields=["status", "decided_by", "date_decided"])

    def _release_stock(self):
        if self.lot_id:
            StockLot.objects.filter(pk=self.lot_id).update(
                quantity=models.F("quantity") + self.quantity
            )
        else:
            ComponentUnit.objects.filter(pk=self.unit_id).update(
                lifecycle=ComponentUnit.AVAILABLE
            )

    @transaction.atomic
    def approve(self, user):
        if not can_approve(user):
            raise ValidationError("You are not allowed to approve requests.")
        if user.pk == self.requested_by_id:
            raise ValidationError("You cannot approve your own request.")
        self._decide(user, self.APPROVED)
        if self.unit_id:
            ComponentUnit.objects.filter(pk=self.unit_id).update(
                lifecycle=ComponentUnit.ISSUED
            )

    @transaction.atomic
    def reject(self, user):
        if not can_approve(user):
            raise ValidationError("You are not allowed to reject requests.")
        self._decide(user, self.REJECTED)
        self._release_stock()

    @transaction.atomic
    def cancel(self, user):
        if user.pk != self.requested_by_id:
            raise ValidationError("Only the requester can cancel a request.")
        self._decide(user, self.CANCELLED)
        self._release_stock()
