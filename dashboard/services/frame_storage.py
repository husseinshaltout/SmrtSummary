from io import BytesIO

import numpy as np
from django.core.files.storage import default_storage


def frames_to_npz_bytes(frames: np.ndarray) -> bytes:
    buffer = BytesIO()
    np.savez_compressed(buffer, frames=frames)
    return buffer.getvalue()


def load_frames_from_storage(name: str) -> np.ndarray:
    with default_storage.open(name, "rb") as handle:
        buffer = handle.read()
    data = np.load(BytesIO(buffer))
    return data["frames"]
