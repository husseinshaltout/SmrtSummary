import os
import tempfile
import time
from contextlib import contextmanager
from urllib.parse import urlparse

import cv2 as cv
import numpy as np
import requests
from django.core.files.storage import default_storage


MAX_FRAMES = 500


@contextmanager
def video_capture(source: str):
    local_path = source
    temp_file = None
    if source.startswith(("http://", "https://")):
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        response = requests.get(source, timeout=120)
        response.raise_for_status()
        temp_file.write(response.content)
        temp_file.close()
        local_path = temp_file.name
    elif not os.path.isfile(source):
        with default_storage.open(source, "rb") as handle:
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            temp_file.write(handle.read())
            temp_file.close()
            local_path = temp_file.name

    cap = cv.VideoCapture(local_path)
    if not cap.isOpened():
        if temp_file:
            os.unlink(temp_file.name)
        raise ValueError(f"unable to open video: {urlparse(source).path or source}")
    try:
        yield cap
    finally:
        cap.release()
        if temp_file:
            os.unlink(temp_file.name)


def get_video_metadata(cap: cv.VideoCapture) -> tuple[str, int, int, float]:
    fps = cap.get(cv.CAP_PROP_FPS) or 30.0
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    if frame_count <= 0 or fps <= 0:
        raise ValueError("video has no readable frames")
    duration = time.strftime("%H:%M:%S", time.gmtime(int(frame_count / fps)))
    return duration, frame_count, frame_width, fps


def extract_frames(cap: cv.VideoCapture, max_frames: int = MAX_FRAMES) -> np.ndarray:
    total = int(cap.get(cv.CAP_PROP_FRAME_COUNT)) or max_frames
    step = max(1, total // max_frames)
    frames = []
    index = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if index % step == 0:
            frames.append(frame)
            if len(frames) >= max_frames:
                break
        index += 1
    if not frames:
        raise ValueError("no frames extracted from video")
    return np.array(frames)
