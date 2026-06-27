from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from .validators import file_size, validate_file_extension


class VideoStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    READY = "ready", "Ready"
    FAILED = "failed", "Failed"


class Video(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=200, blank=True)
    videofile = models.FileField(
        upload_to="videos/%Y/%m/%d/", verbose_name="", validators=[file_size, validate_file_extension]
    )
    thumbnail = models.ImageField(upload_to="photos/thumbnails/%Y/%m/%d/", blank=True)
    video_summary = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    video_duration = models.CharField(max_length=200, blank=True)
    video_frames = models.FileField(upload_to="npz/%Y/%m/%d/", blank=True)
    upload_date = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=20, choices=VideoStatus.choices, default=VideoStatus.PENDING)
    frame_count = models.PositiveIntegerField(default=0)
    frame_width = models.PositiveIntegerField(default=0)
    processing_error = models.TextField(blank=True)

    class Meta:
        ordering = ["-upload_date"]

    def save(self, *args, **kwargs):
        if not self.title and self.videofile:
            self.title = self.videofile.name.split("/")[-1]
        elif not self.title:
            self.title = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}: {self.videofile}"
