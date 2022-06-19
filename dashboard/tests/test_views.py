from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from dashboard.forms import VideoForm
from dashboard.models import Video
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.uploadURL = reverse("upload")
        self.user = get_user_model().objects.create_user(
            username="test", password="12test12", email="test@example.com"
        )
        self.user.save()
        self.client.login(username="test", password="12test12")
        self.videoFile = SimpleUploadedFile(
            "test.mp4",
            open("./dashboard/tests/test.mp4", "rb").read(),
            content_type="video/mp4",
        )
        self.uploader = User.objects.filter(username="test").first()
        self.scanlineValue = {"scanline_slider": "20"}
        return super().setUp()


class UploadTest(BaseTest):
    def test_can_view_page_correctly(self) -> None:
        response = self.client.get(self.uploadURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/upload.html")

    def test_can_upload_file(self) -> None:
        response = self.client.post(self.uploadURL, {"videofile": self.videoFile}, follow=True)
        videoObj = Video.objects.filter(uploaded_by=self.uploader).first()
        self.assertRedirects(response, reverse("scanline", kwargs={"video_id": videoObj.id}))

    def test_upload_page_uses_video_form(self) -> None:
        response = self.client.get(self.uploadURL)
        self.assertIsInstance(response.context["form"], VideoForm)

    def test_user_can_select_scanline(self) -> None:
        self.client.post(self.uploadURL, {"videofile": self.videoFile}, follow=True)
        videoObj = Video.objects.filter(uploaded_by=self.uploader).first()
        response = self.client.post(
            reverse("scanline", kwargs={"video_id": videoObj.id}), self.scanlineValue, format="text/html"
        )
        self.assertRedirects(response, reverse("video_summary", kwargs={"video_id": videoObj.id}))

    def test_unauthorized_user_scanline_video_access(self) -> None:
        videoObj = Video.objects.create(uploaded_by=self.uploader, title="testtest", videofile=self.videoFile)
        self.client.logout()
        self.user = get_user_model().objects.create_user(
            username="test2", password="12test12", email="test2@example.com"
        )
        self.user.save()
        self.client.login(username="test2", password="12test12")
        response = self.client.get(reverse("scanline", kwargs={"video_id": videoObj.id}), format="text/html")
        html = response.content.decode("utf8")
        self.assertIn("<h1>Not authenticated</h1>", html)

    def test_unauthorized_user_video_summary_video_access(self) -> None:
        videoObj = Video.objects.create(uploaded_by=self.uploader, title="testtest", videofile=self.videoFile)
        self.client.logout()
        self.user = get_user_model().objects.create_user(
            username="test2", password="12test12", email="test2@example.com"
        )
        self.user.save()
        self.client.login(username="test2", password="12test12")
        response = self.client.get(reverse("video_summary", kwargs={"video_id": videoObj.id}), format="text/html")
        html = response.content.decode("utf8")
        self.assertIn("<h1>Not authenticated</h1>", html)
