# Generated by Django 4.0.4 on 2022-06-25 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_alter_video_video_frames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_frames',
            field=models.FileField(blank=True, upload_to='hdf5/%Y/%m/%d/'),
        ),
    ]