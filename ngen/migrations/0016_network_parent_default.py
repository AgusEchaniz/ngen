# Generated by Django 3.2.5 on 2021-11-26 15:05

from django.db import migrations

from ngen.models import Network


def set_cidr(apps, schema_editor):
    default_network = Network.objects.get(cidr="0.0.0.0/0")
    for network in Network.objects.all():
        if not network.parent:
            network.parent = default_network
            network.save()


class Migration(migrations.Migration):
    dependencies = [
        ('ngen', '0015_copy_host_to_network'),
    ]

    operations = [
        migrations.RunPython(set_cidr)
    ]
