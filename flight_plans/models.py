from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from applications.models import ReserveAirspace
from rpas.models import RpasModel
from organizations.models import Organization

User = get_user_model()

# Checklist Redesign: Storing templates and submissions as JSON objects
# for simplified integration with the React-based checklist builder.


class DailyWorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reserve_airspace = models.ForeignKey(
        ReserveAirspace, on_delete=models.CASCADE, blank=True, null=True
    )

    project = models.ForeignKey(
        "applications.Project", on_delete=models.CASCADE, blank=True, null=True
    )
    rpas = models.ForeignKey(
        "rpas.Rpas", on_delete=models.CASCADE, blank=True, null=True
    )

    # Performance Metrics
    acres_sprayed = models.FloatField(default=0.0)
    bags_spread = models.FloatField(default=0.0)
    application_rate_spraying = models.FloatField(default=0.0, help_text="in l/ha")
    operation_date = models.DateTimeField(null=True, blank=True)

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, blank=True, null=True
    )

    # New JSON-based Checklist Templates
    preflight_template = models.ForeignKey(
        "ChecklistTemplate",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={"checklist_type": "PRE"},
        related_name="preflight_work_logs",
    )
    preflight_saved_at = models.DateTimeField(blank=True, null=True)
    postflight_template = models.ForeignKey(
        "ChecklistTemplate",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={"checklist_type": "POS"},
        related_name="postflight_work_logs",
    )
    postflight_saved_at = models.DateTimeField(blank=True, null=True)

    preflight_results = models.JSONField(
        help_text="Responses for each item with status and comments",
        blank=True,
        null=True,
    )
    postflight_results = models.JSONField(
        help_text="Responses for each item with status and comments",
        blank=True,
        null=True,
    )

    is_complete = models.BooleanField(default=False)

    def __str__(self):
        if self.reserve_airspace_id is None:
            return f"DailyWorkLog #{self.pk or 'unsaved'}"
        application_number = self.reserve_airspace.application_number
        if application_number:
            return str(application_number)
        return f"ReserveAirspace #{self.reserve_airspace_id}"

    def get_pre_flight_completion(self):
        """Calculates progress based on items submitted for this flight log."""
        if not self.preflight_template:
            return 0

        # New JSON-based completion logic
        submission = self.checklist_submissions.filter(
            template=self.preflight_template, checklist_type="PRE"
        ).last()
        if not submission:
            return 0

        results = submission.results
        if not results:
            return 0

        total_items = 0
        done_items = 0

        # results is expected to look like: {"checklist": {"Pre-Flight": [{"items": [...]}, ...]}}
        # We flattened the logic for completion tracking
        for category in results.get("checklist", {}).values():
            for group in category:
                for item in group.get("items", []):
                    total_items += 1
                    if item.get("status") in ["YES", "N/A"]:
                        done_items += 1

        return (done_items / total_items * 100) if total_items > 0 else 0

    def get_post_flight_completion(self):
        if not self.postflight_template:
            return 0

        submission = self.checklist_submissions.filter(
            template=self.postflight_template, checklist_type="POS"
        ).last()
        if not submission:
            return 0

        results = submission.results
        if not results:
            return 0

        total_items = 0
        done_items = 0

        for category in results.get("checklist", {}).values():
            for group in category:
                for item in group.get("items", []):
                    total_items += 1
                    if item.get("status") in ["YES", "N/A"]:
                        done_items += 1

        return (done_items / total_items * 100) if total_items > 0 else 0

    def save(self, *args, **kwargs):
        if not self.organization and self.user:
            try:
                self.organization = self.user.userprofile.organization
            except:
                pass
        super(DailyWorkLog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("log_detail", kwargs={"pk": self.pk})


class ChecklistTemplate(models.Model):
    CHECKLIST_TYPE_CHOICES = [
        ("PRE", "Pre-Flight"),
        ("POS", "Post-Flight"),
        ("INF", "In-Flight"),
        ("EMR", "Emergency"),
    ]

    title = models.CharField(max_length=100)
    checklist_type = models.CharField(
        max_length=20, choices=CHECKLIST_TYPE_CHOICES, default="PRE"
    )
    rpas_model = models.ForeignKey(
        "rpas.RpasModel",
        on_delete=models.CASCADE,
        related_name="checklist_templates",
        blank=True,
        null=True,
    )
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, blank=True, null=True
    )
    # This field holds the pure structure from the React builder
    checklist_data = models.JSONField(
        help_text="Full template structure in JSON format"
    )

    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        model_name = self.rpas_model.model_name if self.rpas_model else "Generic"
        return f"{self.title} ({self.get_checklist_type_display()}) - {self.created_by.first_name}"

    def save(self, *args, **kwargs):
        if not self.organization and self.created_by:
            try:
                # userprofile exists from the post_save signal in accounts app
                self.organization = self.created_by.userprofile.organization
            except:
                pass
        super().save(*args, **kwargs)
