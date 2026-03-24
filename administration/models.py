import os
from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def expense_receipt_upload_path(instance, filename):
    # This will save the image to media/field_expenses/project_name/user_name/filename
    project_name = instance.project.name.replace(" ", "_")
    user_name = instance.user.username
    return os.path.join("field_expenses", project_name, user_name, filename)


class FieldExpense(models.Model):
    CATEGORY_CHOICES = [
        ("PDMS", "PDMs (Per Diems)"),
        ("GEN FUEL", "Generator Fuel"),
        ("CAR FUEL", "Car Fuel"),
        ("OIL", "Oil"),
        ("FOOD", "Food"),
        ("MAINTENANCE", "Maintenance"),
        ("TRANSPORT", "Transport"),
        ("ACCOMMODATION", "Accommodation"),
        ("KCAA_FEES", "KCAA Fees"),
        ("OTHER", "Other"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="field_expenses"
    )
    project = models.ForeignKey(
        "applications.Project", on_delete=models.CASCADE, related_name="field_expenses"
    )
    description = models.TextField(blank=True, null=True)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    duration_days = models.IntegerField(default=1)

    receipt = models.ImageField(
        upload_to=expense_receipt_upload_path, blank=True, null=True
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.start_date and self.duration_days and not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.duration_days - 1)

        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            # duration_days = (delta.days + 1) because if start and end are same, it's 1 day
            self.duration_days = max(1, delta.days + 1)
        super(FieldExpense, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.name} - {self.category} - {self.user.username}"


class FieldRequisition(models.Model):
    # Similar to FieldExpense, maybe slightly different status
    CATEGORY_CHOICES = FieldExpense.CATEGORY_CHOICES
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="field_requisitions"
    )
    project = models.ForeignKey(
        "applications.Project",
        on_delete=models.CASCADE,
        related_name="field_requisitions",
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    duration_days = models.IntegerField(default=1)

    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")
    status_message = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="approved_requisitions",
        null=True,
        blank=True,
    )
    approved_date = models.DateTimeField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.start_date and self.duration_days and not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.duration_days - 1)

        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.duration_days = max(1, delta.days + 1)
        super(FieldRequisition, self).save(*args, **kwargs)

    def __str__(self):
        return (
            f"Requisition: {self.project.name} - {self.category} - {self.user.username}"
        )
