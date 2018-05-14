from django.db import models
from django.contrib.auth.models import User



class UserToUserMessages(models.Model):
    title = models.CharField(max_length = 120, blank=True, null=True)
    text = models.TextField()
    sender = models.ForeignKey(User)
    receiver = models.ForeignKey(User, related_name='sent_to')

    date_created  = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


