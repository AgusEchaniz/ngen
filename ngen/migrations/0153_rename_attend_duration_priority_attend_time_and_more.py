# Generated by Django 4.0.3 on 2022-04-08 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0152_remove_priority_attend_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='priority',
            old_name='attend_duration',
            new_name='attend_time',
        ),
        migrations.RenameField(
            model_name='priority',
            old_name='solve_duration',
            new_name='solve_time',
        ),
    ]
