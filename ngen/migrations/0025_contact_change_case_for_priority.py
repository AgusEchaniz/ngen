# Generated by Django 3.2.5 on 2021-11-29 22:06

from django.db import migrations


def contact_change_case_for_priority(apps, schema_editor):
    for contact in apps.get_model('ngen', 'Contact').objects.all():
        contact.priority = apps.get_model('ngen', 'IncidentPriority').objects.get(code=contact.contact_case.level)
        contact.save()


class Migration(migrations.Migration):
    dependencies = [
        ('ngen', '0024_auto_20211204_2234'),
    ]

    operations = [
        migrations.RunPython(contact_change_case_for_priority)
    ]