# Generated by Django 4.0.4 on 2022-06-24 06:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_video_videofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_frames',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, size=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='video_duration',
            field=models.CharField(blank=True, default=list, max_length=200),
        ),
    ]
