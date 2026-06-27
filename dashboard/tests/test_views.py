import os
import tempfile

import cv2 as cv
import numpy as np
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from dashboard.forms import VideoForm
from dashboard.models import Video, VideoStatus


def create_test_mp4() -> bytes:
    temp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    writer = cv.VideoWriter(temp.name, cv.VideoWriter_fourcc(*"mp4v"), 10, (160, 120))
    for index in range(5):
        frame = np.full((120, 160, 3), index * 40, dtype=np.uint8)
        writer.write(frame)
    writer.release()
    with open(temp.name, "rb") as handle:
        data = handle.read()
    os.unlink(temp.name)
    return data


@override_settings(
    DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
    MEDIA_ROOT=tempfile.mkdtemp(),
)
class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="test", password="12test12", email="test@example.com")
        self.client.login(username="test", password="12test12")
        self.video_bytes = create_test_mp4()
        self.video_file = SimpleUploadedFile("test.mp4", self.video_bytes, content_type="video/mp4")

    def test_upload_page_renders(self):
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], VideoForm)

    def test_upload_and_process_video(self):
        response = self.client.post(reverse("upload"), {"videofile": self.video_file}, follow=True)
        video = Video.objects.get(uploaded_by=self.user)
        self.assertEqual(video.status, VideoStatus.READY)
        self.assertGreater(video.frame_count, 0)
        self.assertRedirects(response, reverse("scanline", kwargs={"video_id": video.id}))

    def test_scanline_summary_flow(self):
        upload_file = SimpleUploadedFile("test.mp4", self.video_bytes, content_type="video/mp4")
        self.client.post(reverse("upload"), {"videofile": upload_file})
        video = Video.objects.get(uploaded_by=self.user)
        self.assertEqual(video.status, VideoStatus.READY, video.processing_error)
        response = self.client.post(reverse("scanline", kwargs={"video_id": video.id}), {"scanline_slider": "10"})
        video.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("video_summary", kwargs={"video_id": video.id}))
        self.assertTrue(video.video_summary)

    def test_unauthorized_scanline_returns_403(self):
        video = Video.objects.create(
            uploaded_by=self.user,
            title="owned",
            videofile=SimpleUploadedFile("x.mp4", self.video_bytes, content_type="video/mp4"),
            status=VideoStatus.READY,
        )
        other = get_user_model().objects.create_user(username="other", password="12test12", email="o@example.com")
        self.client.logout()
        self.client.login(username="other", password="12test12")
        response = self.client.get(reverse("scanline", kwargs={"video_id": video.id}))
        self.assertEqual(response.status_code, 403)

    def test_video_status_json(self):
        self.client.post(reverse("upload"), {"videofile": self.video_file})
        video = Video.objects.get(uploaded_by=self.user)
        response = self.client.get(reverse("video_status", kwargs={"video_id": video.id}))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], VideoStatus.READY)

    def test_health_endpoint(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
