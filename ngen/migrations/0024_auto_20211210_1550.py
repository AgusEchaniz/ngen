# Generated by Django 3.2.5 on 2021-12-10 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0023_auto_20211210_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident',
            old_name='taxonomy_fake_id',
            new_name='taxonomy',
        ),
        migrations.RenameField(
            model_name='incidentdecision',
            old_name='taxonomy_fake_id',
            new_name='taxonomy',
        ),
        migrations.RenameField(
            model_name='incidentdetected',
            old_name='taxonomy_fake_id',
            new_name='taxonomy',
        ),
        migrations.RenameField(
            model_name='incidentreport',
            old_name='taxonomy_fake_id',
            new_name='taxonomy',
        ),
    ]