# Generated by Django 2.2.10 on 2020-03-05 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0006_postholder_organization'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='kcaa_no',
            new_name='caa_no',
        ),
    ]
