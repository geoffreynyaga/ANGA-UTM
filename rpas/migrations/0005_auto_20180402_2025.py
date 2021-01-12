# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-02 17:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpas', '0004_auto_20180402_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpasmodel',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rpas.Manufacturer'),
        ),
        migrations.AlterField(
            model_name='rpasmodel',
            name='rpas_model_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rpas.RpasModelType'),
        ),
        migrations.AlterField(
            model_name='rpasmodel',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
