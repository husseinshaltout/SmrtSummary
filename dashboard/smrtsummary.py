"""Backward-compatible facade; prefer dashboard.services."""
from dashboard.services.frame_storage import load_frames_from_storage
from dashboard.services.scanline_builder import build_summary_bytes, build_thumbnail_bytes
from dashboard.services.video_service import VideoProcessingService


class SmrtSummary:
    def __init__(self, video_location: str) -> None:
        self.video_location = video_location
        self._service = VideoProcessingService()

    def create_summary(self, scanline_x: int, npz_name: str) -> bytes:
        frames = load_frames_from_storage(npz_name.removeprefix("media/"))
        return build_summary_bytes(frames, scanline_x)

    def create_thumbnail(self, frames_array, thumbnail_frame: int) -> bytes:
        return build_thumbnail_bytes(frames_array, thumbnail_frame)
