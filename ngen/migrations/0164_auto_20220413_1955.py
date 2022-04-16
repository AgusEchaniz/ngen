# Generated by Django 4.0.3 on 2022-04-13 19:55

from django.db import migrations

from ngen.models import Case, State


def state_bools(apps, schema_editor):
    State.objects.filter(name='Initial').update(blocked=False, attended=False, solved=False)
    State.objects.filter(name='Staging').update(blocked=False, attended=False, solved=False)
    State.objects.filter(name='Open').update(blocked=False, attended=True, solved=False)
    State.objects.filter(name='Closed').update(blocked=True, attended=False, solved=True)


def state_translate(name):
    if name in ['Undefined', 'Removed']:
        return 'Staging'
    if name.startswith(('Discarded by', 'Closed by')):
        return 'Closed'
    if name == 'Unresolved':
        return 'Open'
    return name


def state_bool_on_case_dates(apps, schema_editor):
    for case in Case.objects.all():
        for log in case.history.filter(changes__contains='"state"', action=1).order_by('timestamp'):
            child_state = State.objects.get(name=state_translate(log.changes_dict['state'][1]))
            if child_state.attended:
                case.attend_date = log.timestamp
                case.solve_date = None
            if child_state.solved:
                case.solve_date = log.timestamp
        case.save(update_fields=['attend_date', 'solve_date'])


class Migration(migrations.Migration):
    dependencies = [
        ('ngen', '0163_auto_20220413_1819'),
    ]

    operations = [
        migrations.RunPython(state_bools),
        migrations.RunPython(state_bool_on_case_dates)

    ]