from django.conf import settings
from django.db import models
from datetime import datetime
from validator import file_size

class Video(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    videofile = models.FileField(upload_to='videos/%Y/%m/%d/',
                                 verbose_name="Video location",
                                 validators=[file_size])
    video_summary = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title + ": " + str(self.videofile)
