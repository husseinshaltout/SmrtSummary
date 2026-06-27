import logging

from django.conf import settings

from dashboard.models import Video
from dashboard.services import VideoProcessingService

logger = logging.getLogger(__name__)


def process_video_upload(video_id: int) -> None:
    video = Video.objects.get(pk=video_id)
    VideoProcessingService().process_upload(video)


def enqueue_video_processing(video_id: int) -> None:
    if settings.REDIS_URL:
        import django_rq

        django_rq.enqueue(process_video_upload, video_id)
        return
    process_video_upload(video_id)
