# Generated by Django 4.0.4 on 2022-05-17 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0190_remove_event_network'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='notification_count',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]