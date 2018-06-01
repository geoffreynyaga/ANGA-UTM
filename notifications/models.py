from django.db import models
from django.contrib.auth.models import User


class Notifications(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    receiver = models.ForeignKey(User, related_name='send_notification_to')

    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # TODO: Notifications is_read
