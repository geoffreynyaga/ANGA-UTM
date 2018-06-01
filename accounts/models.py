from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from organizations.models import Organization


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(default=models.NOT_PROVIDED, null=True, unique=True, help_text='+254....')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='images/profile_pic', blank=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)
