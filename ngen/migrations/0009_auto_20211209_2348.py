# Generated by Django 3.2.5 on 2021-12-09 22:28

from django.db import migrations


def incident_type_values_to_parent(apps, schema_editor):
    incident_types = apps.get_model('ngen', 'IncidentType')

    for incident_type in incident_types.objects.filter(taxonomyvalue__isnull=False):
        incident_type.parent = incident_types.objects.get(slug=incident_type.taxonomyvalue.slug)
        incident_type.save()


class Migration(migrations.Migration):
    dependencies = [
        ('ngen', '0008_auto_20211209_2326'),
    ]

    operations = [
        migrations.RunPython(
            code=incident_type_values_to_parent,
        ),
    ]
