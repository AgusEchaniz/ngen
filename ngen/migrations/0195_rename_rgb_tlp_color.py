# Generated by Django 4.0.4 on 2022-05-27 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0194_alter_artifact_options_priority_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tlp',
            old_name='rgb',
            new_name='color',
        ),
    ]