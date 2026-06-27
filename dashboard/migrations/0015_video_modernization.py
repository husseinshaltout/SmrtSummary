from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dashboard", "0014_alter_video_video_frames"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="frame_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="video",
            name="frame_width",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="video",
            name="processing_error",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="video",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("processing", "Processing"),
                    ("ready", "Ready"),
                    ("failed", "Failed"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="title",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="video",
            name="upload_date",
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="video",
            name="uploaded_by",
            field=models.ForeignKey(
                db_index=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
