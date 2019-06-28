# Generated by Django 2.2 on 2019-04-27 11:33

from django.db import migrations, models


def copy_program_to_mixin(apps, schema_editor):
    presentation_model = apps.get_model('api', 'Presentation')
    for p in presentation_model.objects.all():
        p.name2_ko = p.name_ko
        p.name2_en = p.name_en
        p.desc2_ko = p.desc_ko
        p.desc2_en = p.desc_en
        p.visible2 = p.visible
        p.language2 = p.language
        p.save()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0067_auto_20190628_1525'),
    ]

    operations = [
        migrations.RunPython(copy_program_to_mixin),
    ]
