# Generated by Django 3.2.5 on 2021-12-10 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0021_alter_taxonomy_parent_auto_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taxonomy',
            old_name='parent_auto_id',
            new_name='parent',
        ),
    ]