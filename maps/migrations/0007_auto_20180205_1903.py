# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-05 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_auto_20180205_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationpoints',
            name='name',
            field=models.CharField(max_length=120),
        ),
    ]
