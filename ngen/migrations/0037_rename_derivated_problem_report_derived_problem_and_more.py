# Generated by Django 4.0 on 2021-12-21 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0036_alter_contact_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='derivated_problem',
            new_name='derived_problem',
        ),
        migrations.RenameField(
            model_name='report',
            old_name='recomendations',
            new_name='recommendations',
        ),
    ]