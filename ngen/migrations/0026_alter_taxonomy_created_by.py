# Generated by Django 3.2.5 on 2021-12-10 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0025_auto_20211210_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxonomy',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user'),
        ),
    ]
