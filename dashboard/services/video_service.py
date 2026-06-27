import logging

from django.core.files.base import ContentFile

from dashboard.models import Video, VideoStatus

from .frame_extractor import extract_frames, get_video_metadata, video_capture
from .frame_storage import frames_to_npz_bytes, load_frames_from_storage
from .scanline_builder import build_summary_bytes, build_thumbnail_bytes

logger = logging.getLogger(__name__)


class VideoProcessingService:
    def process_upload(self, video: Video) -> None:
        video.status = VideoStatus.PROCESSING
        video.processing_error = ""
        video.save(update_fields=["status", "processing_error"])
        try:
            source = video.videofile.url if video.videofile.url.startswith("http") else video.videofile.name
            with video_capture(source) as cap:
                duration, frame_count, frame_width, fps = get_video_metadata(cap)
                frames = extract_frames(cap)
            video.video_duration = duration
            video.frame_count = len(frames)
            video.frame_width = frame_width if frame_width else frames.shape[2]
            npz_bytes = frames_to_npz_bytes(frames)
            npz_name = f"{video.uploaded_by_id}_{video.videofile.name.split('/')[-1]}.npz"
            video.video_frames.save(npz_name, ContentFile(npz_bytes), save=False)
            thumb_index = len(frames) // 2
            thumb_bytes = build_thumbnail_bytes(frames, thumb_index)
            video.thumbnail.save("thumbnail.jpg", ContentFile(thumb_bytes), save=False)
            video.status = VideoStatus.READY
            video.save()
        except Exception as exc:
            logger.exception("video processing failed for video %s", video.pk)
            video.status = VideoStatus.FAILED
            video.processing_error = str(exc)
            video.save(update_fields=["status", "processing_error"])
            raise

    def create_scanline_summary(self, video: Video, scanline_x: int) -> bytes:
        if not video.video_frames:
            raise ValueError("video frames not available")
        frames = load_frames_from_storage(video.video_frames.name)
        return build_summary_bytes(frames, scanline_x)
