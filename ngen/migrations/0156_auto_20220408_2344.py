# Generated by Django 4.0.3 on 2022-04-08 23:44

from django.db import migrations


def remove_undefined_priority(apps, schema_editor):
    Priority = apps.get_model('ngen', 'Priority')
    priority = Priority.objects.get(name='Undefined')
    if priority:
        for case in Priority.objects.get(name='Undefined').case_set.all():
            case.priority = Priority.objects.get(name='Very Low')
            case.save()
        priority.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('ngen', '0155_priority_attend_deadline_priority_solve_deadline'),
    ]

    operations = [
        migrations.RunPython(remove_undefined_priority),
    ]
