# Generated by Django 4.0.3 on 2022-04-04 01:29

from django.db import migrations


def state_change_orphan_delete(apps, schema_editor):
    IncidentStateChange = apps.get_model('ngen', 'IncidentStateChange')
    Case = apps.get_model('ngen', 'Case')
    for state_change in IncidentStateChange.objects.all():
        try:
            Case.objects.get(pk=state_change.case)
        except:
            state_change.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('ngen', '0144_rename_incident_id_incidentstatechange_case'),
    ]

    operations = [
        migrations.RunPython(state_change_orphan_delete),
    ]