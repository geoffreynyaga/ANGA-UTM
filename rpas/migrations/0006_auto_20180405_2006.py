# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-05 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpas', '0005_auto_20180402_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payload',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rpas.Manufacturer'),
        ),
        migrations.AlterField(
            model_name='payload',
            name='payload_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rpas.PayloadModel'),
        ),
        migrations.AlterField(
            model_name='payload',
            name='payload_serial',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='rpas',
            name='rpas_serial',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
