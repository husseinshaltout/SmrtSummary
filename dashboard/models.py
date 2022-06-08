from django.db import models
from datetime import datetime
from .validators import file_size
from django.contrib.auth.models import User


class Video(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default=datetime.now)
    videofile = models.FileField(upload_to='videos/%Y/%m/%d/',
                                 verbose_name="",
                                 validators=[file_size])
    thumbnail = models.ImageField(upload_to='photos/thumbnails/%Y/%m/%d/',
                                  blank=True)
    video_summary = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    video_duration = models.CharField(max_length=200, blank=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title + ": " + str(self.videofile)
