import dashboard.validators
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
            name="Video",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=200)),
                (
                    "videofile",
                    models.FileField(
                        upload_to="videos/%Y/%m/%d/",
                        validators=[dashboard.validators.file_size, dashboard.validators.validate_file_extension],
                        verbose_name="",
                    ),
                ),
                ("thumbnail", models.ImageField(blank=True, upload_to="photos/thumbnails/%Y/%m/%d/")),
                ("video_summary", models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/")),
                ("video_duration", models.CharField(blank=True, max_length=200)),
                ("video_frames", models.FileField(blank=True, upload_to="npz/%Y/%m/%d/")),
                ("upload_date", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "status",
                    models.CharField(
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
                ("frame_count", models.PositiveIntegerField(default=0)),
                ("frame_width", models.PositiveIntegerField(default=0)),
                ("processing_error", models.TextField(blank=True)),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        db_index=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-upload_date"],
            },
        ),
    ]
