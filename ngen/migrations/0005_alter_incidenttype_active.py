# Generated by Django 3.2.5 on 2021-12-09 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0004_alter_incidenttype_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidenttype',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
