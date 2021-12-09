# Generated by Django 3.2.5 on 2021-12-05 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0032_alter_contact_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='contact_type',
            new_name='type',
        ),
        migrations.AlterField(
            model_name='network',
            name='type',
            field=models.CharField(choices=[('internal', 'internal'), ('external', 'external')], default='internal', max_length=20),
        ),
    ]