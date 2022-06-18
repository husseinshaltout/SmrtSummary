from django.test import TestCase
from django.urls import reverse
from dashboard.models import Video
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.registerURL = reverse("register")
        self.uploadURL = reverse("upload")
        self.user = {
            "firstname": "TestFirstName",
            "lastname": "TestLastName",
            "username": "username",
            "email": "username@email.com",
            "password": "password",
            "password2": "password",
        }
        self.client.post(self.registerURL, self.user, format="text/html")
        user = User.objects.filter(email=self.user["email"]).first()
        videoFile = SimpleUploadedFile(
            "test.mp4", open("./dashboard/tests/test.mp4", "rb").read(), content_type="video/mp4"
        )
        Video.objects.create(uploaded_by=user, videofile=videoFile)
        return super().setUp()


class VideoModelTest(BaseTest):
    def test_object_name_is_title_colon_videofile(self):
        video = Video.objects.get(id=1)
        expected_object_name = f"{video.title}: {video.videofile}"
        self.assertEqual(str(video), expected_object_name)
