import unittest
import numpy as np
from PIL import Image
from palette import extract_palette


class PaletteTests(unittest.TestCase):
    def test_similar_tones_are_merged(self):
        image = Image.new('RGB', (200, 100))
        pixels = np.empty((100, 200, 3), dtype=np.uint8)
        pixels[:50, :100] = (201, 25, 56)
        pixels[:50, 100:] = (197, 29, 54)
        pixels[50:, :100] = (28, 88, 49)
        pixels[50:, 100:] = (32, 85, 52)
        image = Image.fromarray(pixels)
        palette = extract_palette(image)
        self.assertEqual(len(palette), 2)
        self.assertAlmostEqual(sum(p['percentage'] for p in palette), 100, delta=0.3)

    def test_limited_to_five_colors(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                  (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        data = np.zeros((60, 60, 3), dtype=np.uint8)
        for idx, color in enumerate(colors):
            data[idx * 10:(idx + 1) * 10, :] = color
        palette = extract_palette(Image.fromarray(data))
        self.assertLessEqual(len(palette), 5)
        self.assertLess(sum(c['percentage'] for c in palette), 100)


if __name__ == '__main__':
    unittest.main()
