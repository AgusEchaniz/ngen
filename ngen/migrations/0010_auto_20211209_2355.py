# Generated by Django 3.2.5 on 2021-12-09 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngen', '0009_auto_20211209_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taxonomyvalue',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='taxonomyvalue',
            name='taxonomypredicate',
        ),
        migrations.RemoveField(
            model_name='incidenttype',
            name='taxonomyvalue',
        ),
        migrations.DeleteModel(
            name='TaxonomyPredicate',
        ),
        migrations.DeleteModel(
            name='TaxonomyValue',
        ),
    ]
