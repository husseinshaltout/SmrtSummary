import numpy as np
from django.test import TestCase

from dashboard.services.scanline_builder import build_summary_bytes, build_thumbnail_bytes, clamp_scanline_x


class ScanlineBuilderTests(TestCase):
    def test_clamp_scanline_x(self):
        self.assertEqual(clamp_scanline_x(5, 100), 5)
        self.assertEqual(clamp_scanline_x(-1, 100), 0)
        self.assertEqual(clamp_scanline_x(200, 100), 99)

    def test_build_summary_width_matches_frame_count(self):
        frames = np.zeros((10, 48, 64, 3), dtype=np.uint8)
        for index in range(10):
            frames[index, :, index % 64, :] = 255
        summary_bytes = build_summary_bytes(frames, 10)
        self.assertGreater(len(summary_bytes), 0)
        from io import BytesIO
        from PIL import Image

        image = Image.open(BytesIO(summary_bytes))
        self.assertEqual(image.size[0], 10)
        self.assertEqual(image.size[1], 48)

    def test_build_thumbnail_returns_jpeg(self):
        frames = np.zeros((3, 10, 10, 3), dtype=np.uint8)
        thumb = build_thumbnail_bytes(frames, 1)
        self.assertEqual(thumb[:2], b"\xff\xd8")
