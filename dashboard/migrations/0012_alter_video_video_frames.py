# Generated by Django 4.0.4 on 2022-06-24 11:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_alter_video_video_duration_alter_video_video_frames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_frames',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), null=True, size=None), null=True, size=None),
        ),
    ]
