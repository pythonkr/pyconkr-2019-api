# Generated by Django 2.1.5 on 2019-02-06 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('name_ko', models.CharField(db_index=True, max_length=100, null=True)),
                ('name_en', models.CharField(db_index=True, max_length=100, null=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=50)),
                ('name_ko', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('name_en', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('conference_started_at', models.DateField(null=True)),
                ('conference_finished_at', models.DateField(null=True)),
                ('sprint_started_at', models.DateField(null=True)),
                ('sprint_finished_at', models.DateField(null=True)),
                ('tutorial_started_at', models.DateField(null=True)),
                ('tutorial_finished_at', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('name_ko', models.CharField(db_index=True, max_length=100, null=True)),
                ('name_en', models.CharField(db_index=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=50)),
                ('name_ko', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('name_en', models.CharField(blank=True, default='', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('name_ko', models.CharField(blank=True, max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('desc_ko', models.TextField(blank=True, null=True)),
                ('desc_en', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField(default=0)),
                ('visible', models.BooleanField(default=False)),
                ('language', models.CharField(choices=[('E', 'English'), ('K', 'Korean')], default='K', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('program_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.Program')),
                ('accepted', models.BooleanField(default=False)),
                ('started_at', models.DateTimeField(null=True)),
                ('finished_at', models.DateTimeField(null=True)),
                ('slide_url', models.CharField(blank=True, max_length=255, null=True)),
                ('pdf_url', models.CharField(blank=True, max_length=255, null=True)),
                ('video_url', models.CharField(blank=True, max_length=255, null=True)),
                ('recordable', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Category')),
                ('difficulty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Difficulty')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Place')),
            ],
            bases=('api.program',),
        ),
    ]
