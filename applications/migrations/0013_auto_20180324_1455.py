# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-24 11:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0012_reserveairspace_objective'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reserveairspace',
            old_name='objective',
            new_name='mission_type',
        ),
    ]
