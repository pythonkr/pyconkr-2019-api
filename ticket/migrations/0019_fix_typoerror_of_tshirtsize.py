# Generated by Django 2.2 on 2019-04-27 11:33

from django.db import migrations, models


def fix_tshirtsize(apps, schema_editor):
    ticket_model = apps.get_model('ticket', 'Ticket')
    replace_map = {
        'S(85)': 'S(90)',
        'M(90)': 'M(95)',
        'L(95)': 'L(100)',
        'XL(100)': 'XL(105)',
        '2XL(105)': '2XL(110)',
        '3XL(110)': '3XL(115)',
        '4XL(115)': '4XL(120)'
    }
    for t in ticket_model.objects.all():
        if isinstance(t.options, str):
            continue
        if 'tshirtsize' in t.options:
            old = t.options['tshirtsize']
            t.options['tshirtsize'] = replace_map[old]
            t.save()


class Migration(migrations.Migration):
    dependencies = [
        ('ticket', '0018_auto_20190702_1533'),
    ]

    operations = [
        migrations.RunPython(fix_tshirtsize),
    ]