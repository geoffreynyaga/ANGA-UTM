from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse


class OrganizationDetails(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    website = models.URLField()
    logo = models.ImageField(upload_to="images/logo", blank=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    organization_details = models.OneToOneField(
        OrganizationDetails, on_delete=models.CASCADE
    )
    users = models.ManyToManyField(User)
    ORGANIZATION_TYPE = (
        ("ROC", "ROC"),
        ("REC", "RECREATIONAL"),
        ("PVT", "PRIVATE"),
        ("ATO", "Training Organization"),
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

        elif self.organization_type == "ATO":
            x = "CAA/ATO/"
            y = self.pk
            self.caa_no = x + str(y)

        elif self.organization_type == "CLB":
            x = "CAA/CLB/"
            y = self.pk
            self.caa_no = x + str(y)

        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return self.caa_no


class PostHolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, blank=True, null=True
    )

    ROLES = (
        ("ORD", "Ordinary"),
        ("Man", "Manager"),
        ("PIC", "Pilot in Command"),
        ("HOT", "Head of Training"),
        ("TEC", "Technical"),
    )
    role = models.CharField(max_length=3, choices=ROLES, default=ROLES[1][1])

    def __str__(self):
        return self.role

    def get_absolute_url(self):
        return reverse("all_company_flight_logs")

    def clean(self):
        """ Need to remove the blank=True and null=True in organization as this will bring logical proborganizationlems
            when trying to use clean and validation for both postholder and organization

            --FIXED by using the clean method below to ascertain organization is an input
        """
        if not self.organization:
            raise ValidationError("Kindly select the organization from the dropdown")

        if self.user and self.organization:
            """ Doesnt make sense having the if statement cz user must be input and the above clean method
                ascertains there must be an organization
            """
            x = PostHolder.objects.filter(user=self.user)
            for posthold in x:
                if (
                    posthold.role == self.role
                    and posthold.organization == self.organization
                ):
                    raise ValidationError("This user has this position already!")

    def save(self, *args, **kwargs):

        from notifications.models import Notifications

        Notifications.objects.create(title="New Position", receiver=self.user)

        super(PostHolder, self).save(*args, **kwargs)
