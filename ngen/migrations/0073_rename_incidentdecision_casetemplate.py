# Generated by Django 4.0.1 on 2022-01-10 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0072_alter_tlp_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='IncidentDecision',
            new_name='CaseTemplate',
        ),
    ]
