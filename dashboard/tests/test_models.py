from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from dashboard.models import Video


class VideoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="modeluser", password="pass", email="m@example.com")
        self.video = Video.objects.create(
            uploaded_by=self.user,
            videofile=SimpleUploadedFile("clip.mp4", b"fake", content_type="video/mp4"),
        )

    def test_object_name_is_title_colon_videofile(self):
        expected_object_name = f"{self.video.title}: {self.video.videofile}"
        self.assertEqual(str(self.video), expected_object_name)
