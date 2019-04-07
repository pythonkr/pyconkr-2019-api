# Generated by Django 2.1.5 on 2019-04-06 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20190406_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorlevel',
            name='open_lunch',
            field=models.CharField(blank=True, default='', help_text='열린 점심 정보, 제공되지 않을 경우 공백', max_length=100),
        ),
        migrations.AlterField(
            model_name='sponsorlevel',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='sponsorlevel',
            name='name_en',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sponsorlevel',
            name='name_ko',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]