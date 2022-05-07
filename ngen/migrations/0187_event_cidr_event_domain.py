# Generated by Django 4.0.4 on 2022-05-06 22:15

from django.db import migrations, models
import netfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0186_artifactenrichment_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cidr',
            field=netfields.fields.CidrAddressField(max_length=43, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='event',
            name='domain',
            field=models.CharField(default=None, max_length=255, null=True, unique=True),
        ),
    ]
