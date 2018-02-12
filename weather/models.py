from django.db import models

# Create your models here.

class Reading(models.Model):
    location = models.CharField(max_length = 100)
    weather = models.CharField(max_length = 20)
    wind_str = models.CharField(max_length = 100)
    temp = models.IntegerField()
    humidity = models.CharField(max_length = 100)
    precip = models.CharField(max_length = 100)
    icon_url = models.URLField()
    observation_time = models.CharField(max_length = 100)

