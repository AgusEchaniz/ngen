# Generated by Django 4.0 on 2021-12-24 18:09

from django.db import migrations


def add_edge_fake_id(apps, schema_editor):
    edges = apps.get_model('ngen', 'StateEdge')
    for edge in edges.objects.all():
        edge.parent = edge.oldstate.fake_id
        edge.child = edge.newstate.fake_id
        edge.save()


def add_behavior_fake_id(apps, schema_editor):
    states = apps.get_model('ngen', 'IncidentState')
    for state in states.objects.all():
        state.fake_behavior = state.behavior.fake_id
        state.save()


class Migration(migrations.Migration):
    dependencies = [
        ('ngen', '0041_alter_stateedge_newstate_alter_stateedge_oldstate'),
    ]

    operations = [
        migrations.RunPython(
            code=add_edge_fake_id,
        ),
        migrations.RunPython(
            code=add_behavior_fake_id,
        ),
    ]
