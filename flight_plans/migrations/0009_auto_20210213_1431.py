# Generated by Django 2.2.16 on 2021-02-13 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight_plans', '0008_checklistgroup_checklistitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistitem',
            name='description',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
    ]