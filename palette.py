"""Fast dominant-colour extraction with perceptual shade merging."""

import numpy as np
from PIL import Image
import colornames  # pip install pycolornames


def _to_oklab(rgb):
    """Convert an sRGB colour (0-255) to perceptual OKLab coordinates."""
    rgb = np.asarray(rgb, dtype=np.float64) / 255.0
    linear = np.where(
        rgb <= 0.04045,
        rgb / 12.92,
        ((rgb + 0.055) / 1.055) ** 2.4,
    )
    r, g, b = linear

    l = np.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = np.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = np.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)

    return np.array([
        0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
        1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s,
    ])


def extract_palette(image: Image.Image, count=5, merge_distance=0.08):
    """Return at most `count` dominant colours, merging perceptually close tones.

    `percentage` always measures the fraction of the WHOLE image; since only
    the largest groups are returned, percentages need not add up to 100.
    """
    small = image.convert("RGB").copy()
    small.thumbnail((128, 128), Image.Resampling.BOX)
    total_pixels = small.width * small.height
    if not total_pixels:
        return []

    # Quantise first, so we only need to compare ~32 colours, not every pixel.
    quantized = small.quantize(
        colors=32,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )
    palette = quantized.getpalette()
    entries = []
    for pixels, index in quantized.getcolors(maxcolors=256):
        rgb = np.asarray(palette[index * 3:index * 3 + 3], dtype=np.float64)
        entries.append((pixels, rgb))

    # Large clusters first. Weighted centroids combine near-identical shades.
    groups = []
    for pixels, rgb in sorted(entries, key=lambda entry: entry[0], reverse=True):
        lab = _to_oklab(rgb)
        closest = None
        smallest_distance = float("inf")

        for group in groups:
            centre = group["lab_sum"] / group["pixels"]
            distance = float(np.linalg.norm(lab - centre))
            if distance < smallest_distance:
                closest = group
                smallest_distance = distance

        if closest is not None and smallest_distance < merge_distance:
            closest["pixels"] += pixels
            closest["rgb_sum"] += rgb * pixels
            closest["lab_sum"] += lab * pixels
        else:
            groups.append({
                "pixels": pixels,
                "rgb_sum": rgb * pixels,
                "lab_sum": lab * pixels,
            })

    groups.sort(key=lambda group: group["pixels"], reverse=True)
    result = []
    for group in groups[:count]:
        rgb = np.rint(group["rgb_sum"] / group["pixels"]).astype(int)
        hex_color = "#{:02X}{:02X}{:02X}".format(*rgb)
        result.append({
            "hex": hex_color,
            "name": colornames.find(hex_color),
            "percentage": round(100 * group["pixels"] / total_pixels, 1),
        })
    return result
