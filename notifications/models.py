from django.db import models
from django.contrib.auth.models import User


class Notifications(models.Model):
    class Meta:
        """Meta definition for Notifications."""

        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    title = models.CharField(max_length=120, blank=True, null=True)
    receiver = models.ForeignKey(
        User, related_name="send_notification_to", on_delete=models.CASCADE
    )

    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
