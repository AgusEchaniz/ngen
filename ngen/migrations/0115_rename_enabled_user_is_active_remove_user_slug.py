# Generated by Django 4.0.1 on 2022-01-26 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0114_rename_firstname_user_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='enabled',
            new_name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='slug',
        ),
    ]
