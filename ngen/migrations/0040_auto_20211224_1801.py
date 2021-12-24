# Generated by Django 4.0 on 2021-12-24 18:01

from django.db import migrations


def add_state_auto_id(apps, schema_editor):
    states = apps.get_model('ngen', 'IncidentState')
    for n, state in enumerate(states.objects.all()):
        state.fake_id = n + 1
        state.save()


def add_behavior_auto_id(apps, schema_editor):
    behaviors = apps.get_model('ngen', 'StateBehavior')
    for n, behavior in enumerate(behaviors.objects.all()):
        behavior.fake_id = n + 1
        behavior.save()


class Migration(migrations.Migration):
    dependencies = [
        ('ngen', '0039_alter_contact_created_by_alter_contact_public_key_and_more'),
    ]

    operations = [
        migrations.RunPython(
            code=add_behavior_auto_id,
        ),
        migrations.RunPython(
            code=add_state_auto_id,
        ),
    ]
