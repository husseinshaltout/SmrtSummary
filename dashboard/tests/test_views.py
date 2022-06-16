from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from dashboard.forms import VideoForm


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.registerURL = reverse("register")
        self.uploadURL = reverse("upload")
        self.scanlineURL = "/dashboard/2"
        self.user = {
            "firstname": "TestFirstName",
            "lastname": "TestLastName",
            "username": "username",
            "email": "username@email.com",
            "password": "password",
            "password2": "password",
        }
        self.videoFile = SimpleUploadedFile(
            "test.mp4",
            open("C:/Users/Dell/Documents/GitHub/SmrtSummary/test.mp4", "rb").read(),
            content_type="video/mp4",
        )

        return super().setUp()


class UploadTest(BaseTest):
    def test_can_view_page_correctly(self) -> None:
        self.client.post(self.registerURL, self.user, format="text/html")
        response = self.client.get(self.uploadURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/upload.html")

    def test_can_upload_file(self) -> None:
        self.client.post(self.registerURL, self.user, format="text/html")
        response = self.client.post(self.uploadURL, {"videofile": self.videoFile})
        self.assertRedirects(response, self.scanlineURL)

    def test_upload_page_uses_video_form(self) -> None:
        self.client.post(self.registerURL, self.user, format="text/html")
        response = self.client.get(self.uploadURL)
        self.assertIsInstance(response.context["form"], VideoForm)

    # def test_video_form(self) -> None:
    #     self.client.post(self.registerURL, self.user, format="text/html")
    #     # user = User.objects.filter(email=self.user['email']).first()
    #     # response = self.client.post(self.uploadURL,
    #     #                             {'video': self.videoFile})
    #     request = HttpRequest()
    #     request.POST = {"videofile": self.videoFile}
    #     form = VideoForm(request.POST)
    #     self.assertTrue(form.is_valid())

    # def test_unauthorized_user_scanline_video_access(self) -> None:
    #     response = self.client.get(self.scanlineURL, format="text/html")
    #     print(response.content)
    #     self.assertHTMLEqual(response.content, "<h1>Not authenticated</h1>")
