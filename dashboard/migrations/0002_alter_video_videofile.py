# Generated by Django 4.0.4 on 2022-06-04 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='videofile',
            field=models.FileField(upload_to='videos/%Y/%m/%d/', verbose_name='Video location'),
        ),
    ]