import cv2 as cv
import numpy as np
from io import BytesIO
from PIL import Image


def clamp_scanline_x(scanline_x: int, frame_width: int) -> int:
    if frame_width <= 0:
        raise ValueError("frame_width must be positive")
    return max(0, min(scanline_x, frame_width - 1))


def crop_scanline_columns(frames: np.ndarray, scanline_x: int) -> np.ndarray:
    """Return shape (H, N, 3) BGR summary image."""
    x = clamp_scanline_x(scanline_x, frames.shape[2])
    height, count = frames.shape[1], frames.shape[0]
    summary_bgr = np.zeros((height, count, 3), dtype=frames.dtype)
    for index in range(count):
        summary_bgr[:, index, :] = frames[index, :, x, :]
    return summary_bgr


def build_summary_bytes(frames: np.ndarray, scanline_x: int) -> bytes:
    if frames.size == 0:
        raise ValueError("cannot build summary from empty frames")
    summary_bgr = crop_scanline_columns(frames, scanline_x)
    summary_rgb = cv.cvtColor(summary_bgr, cv.COLOR_BGR2RGB)
    stream = BytesIO()
    Image.fromarray(summary_rgb).save(stream, format="jpeg")
    return stream.getvalue()


def build_thumbnail_bytes(frames: np.ndarray, frame_index: int) -> bytes:
    if frames.size == 0:
        raise ValueError("cannot build thumbnail from empty frames")
    index = max(0, min(frame_index, len(frames) - 1))
    thumb_rgb = cv.cvtColor(frames[index], cv.COLOR_BGR2RGB)
    stream = BytesIO()
    Image.fromarray(thumb_rgb).save(stream, format="jpeg")
    return stream.getvalue()
