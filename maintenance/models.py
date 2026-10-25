from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models, transaction

from inventory.models import ComponentRequest, ComponentUnit


class MaintenanceRecord(models.Model):
    """Work done on a drone, with the components fitted and the signed report."""

    SCHEDULED = "scheduled"
    REPAIR = "repair"
    INSPECTION = "inspection"
    SERVICE_TYPE_CHOICES = (
        (SCHEDULED, "Scheduled service"),
        (REPAIR, "Repair"),
        (INSPECTION, "Inspection"),
    )

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    rpas = models.ForeignKey(
        "rpas.Rpas", on_delete=models.PROTECT, related_name="maintenance_records"
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+"
    )
    date_performed = models.DateField()
    service_type = models.CharField(
        max_length=12, choices=SERVICE_TYPE_CHOICES, default=SCHEDULED
    )
    description = models.TextField(help_text="Work carried out")
    report = models.FileField(
        upload_to="maintenance/reports",
        blank=True,
        validators=[FileExtensionValidator(["pdf"])],
        help_text="Completed report from the template, with photos, as a PDF",
    )
    component_requests = models.ManyToManyField(
        ComponentRequest,
        blank=True,
        related_name="maintenance_records",
        help_text="Approved requests whose components were fitted during this work",
    )
    serviced_units = models.ManyToManyField(
        ComponentUnit,
        blank=True,
        related_name="maintenance_records",
        help_text="Tracked units serviced during this work, e.g. batteries",
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_performed", "-date_created")

    def __str__(self):
        return f"{self.get_service_type_display()} on {self.rpas} ({self.date_performed})"

    @classmethod
    @transaction.atomic
    def record(cls, *, performed_by, rpas, component_requests=(), serviced_units=(), **fields):
        """Save the record, mark requested components as installed on the drone
        and update the last serviced date of serviced units."""
        organization = performed_by.userprofile.organization
        if rpas.organization_id != organization.pk:
            raise ValidationError("The drone belongs to another organization.")
        for component_request in component_requests:
            if component_request.organization_id != organization.pk:
                raise ValidationError("A request belongs to another organization.")
            if component_request.status != ComponentRequest.APPROVED:
                raise ValidationError(
                    f"Request for {component_request.component_type.name} is not approved "
                    "or has already been installed."
                )
            if component_request.rpas_id != rpas.pk:
                raise ValidationError(
                    f"Request for {component_request.component_type.name} was made "
                    "for another drone."
                )
        for unit in serviced_units:
            if unit.organization_id != organization.pk:
                raise ValidationError("A unit belongs to another organization.")

        maintenance_record = cls.objects.create(
            organization=organization, rpas=rpas, performed_by=performed_by, **fields
        )
        maintenance_record.component_requests.set(component_requests)
        maintenance_record.serviced_units.set(serviced_units)

        ComponentRequest.objects.filter(
            pk__in=[r.pk for r in component_requests]
        ).update(status=ComponentRequest.INSTALLED)
        ComponentUnit.objects.filter(
            pk__in=[r.unit_id for r in component_requests if r.unit_id]
        ).update(lifecycle=ComponentUnit.INSTALLED, rpas=rpas)
        # A record entered late must not replace a more recent service date
        ComponentUnit.objects.filter(pk__in=[u.pk for u in serviced_units]).filter(
            models.Q(last_serviced__isnull=True)
            | models.Q(last_serviced__lt=maintenance_record.date_performed)
        ).update(last_serviced=maintenance_record.date_performed)
        return maintenance_record
