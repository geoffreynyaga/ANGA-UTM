# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-28 09:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0013_auto_20180324_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserveairspace',
            name='log',
            field=models.FileField(blank=True, null=True, upload_to='mission-planner-logs/'),
        ),
    ]