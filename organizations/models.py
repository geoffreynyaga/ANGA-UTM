from django.db import models

from django.contrib.auth.models import User


class OrganizationDetails(models.Model):
    name = models.CharField(max_length = 100, unique=True)
    city = models.CharField(max_length = 100)
    website = models.URLField()
    logo = models.ImageField(upload_to = 'images/logo', blank=True)

    def __str__(self):
    	return self.name

class Organization(models.Model):
    organization_details = models.OneToOneField(OrganizationDetails,on_delete = models.CASCADE)
    users = models.ManyToManyField(User)
    ORGANIZATION_TYPE = (
            ('ROC', 'ROC'),
            ('REC', 'RECREATIONAL'),
            ('PVT', 'PRIVATE'),
            ('ATO', 'Training Organization'),
            ('CLB', 'RC Club'),

        )
    organization_type = models.CharField(max_length=3, choices=ORGANIZATION_TYPE,null=True)
    kcaa_no = models.CharField(max_length = 50, unique=True)

    def save(self, *args, **kwargs):
        x = "RPAS/ROC/"
        y = self.kcaa_no
        self.kcaa_no = x + str(y)
        super(Organization,self).save(*args,**kwargs)

    def __str__(self):
    	return self.kcaa_no
