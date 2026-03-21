# from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

# User = get_user_model()


class OrganizationDetails(models.Model):
    class Meta:
        """Meta definition for OrganizationDetails."""

        verbose_name = "Organization Detail"
        verbose_name_plural = "Organization Details"

    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    website = models.URLField()
    logo = models.ImageField(upload_to="images/logo", blank=True)

    def __str__(self):
        return self.name

    def get_logo_re_path(self):
        return self.logo.url


class Organization(models.Model):
    organization_details = models.OneToOneField(
        OrganizationDetails, on_delete=models.CASCADE
    )
    # users = models.ManyToManyField(User, blank=True)
    ORGANIZATION_TYPE = (
        ("ROC", "ROC"),
        ("REC", "RECREATIONAL"),
        ("PVT", "PRIVATE"),
        ("UTO", "Training Organization"),
        ("CLB", "RC Club"),
    )
    organization_type = models.CharField(
        max_length=3, choices=ORGANIZATION_TYPE, null=True
    )
    caa_no = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        super(Organization, self).save(*args, **kwargs)

        if self.organization_type == "ROC":
            x = "CAA/ROC/"
            y = self.pk
            self.caa_no = x + str(y)

        elif self.organization_type == "REC":
            x = "CAA/REC/"
            y = self.pk
            self.caa_no = x + str(y)

        elif self.organization_type == "PVT":
            x = "CAA/PVT/"
            y = self.pk
            self.caa_no = x + str(y)

        elif self.organization_type == "UTO":
            x = "CAA/UTO/"
            y = self.pk
            self.caa_no = x + str(y)

        elif self.organization_type == "CLB":
            x = "CAA/CLB/"
            y = self.pk
            self.caa_no = x + str(y)

        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return self.caa_no
