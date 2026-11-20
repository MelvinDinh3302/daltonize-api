
import numpy as np
from PIL import Image

# Chromium 138.0.7204.97 coefficients in RGB row order.
# Each triple contains the quadratic, linear, and constant terms.
SIMULATION = {
    "p": [
        (0.4720, -1.2946, 0.9857), (-0.6128, 1.6326, 0.0187), (0.1407, -0.3380, -0.0044),
        (-0.1420, 0.2488, 0.0044), (0.1872, -0.3908, 0.9942), (-0.0451, 0.1420, 0.0013),
        (0.0222, -0.0253, -0.0004), (-0.0290, -0.0201, 0.0006), (0.0068, 0.0454, 0.9990),
    ],
    "d": [
        (0.5442, -1.1454, 0.9818), (-0.7091, 1.5287, 0.0238), (0.1650, -0.3833, -0.0055),
        (-0.1664, 0.4368, 0.0056), (0.2178, -0.5327, 0.9927), (-0.0514, 0.0958, 0.0017),
        (0.0180, -0.0288, -0.0006), (-0.0232, -0.0649, 0.0007), (0.0052, 0.0360, 0.9998),
    ],
    "t": [
        (0.4275, -0.0181, 0.9307), (-0.2454, 0.0013, 0.0827), (-0.1821, 0.0168, -0.0134),
        (-0.1280, 0.0047, 0.0202), (0.0233, -0.0398, 0.9728), (0.1048, 0.0352, 0.0070),
        (-0.0156, 0.0061, 0.0071), (0.3841, 0.2947, 0.0151), (-0.3685, -0.3008, 0.9778),
    ],
}
AXIS = {"p": 0, "d": 1, "t": 2}


def chromium_daltonize(image, color_deficit, severity):
    """Apply Chromium's matrix to an RGB Pillow image with sRGB values."""
    if severity == 0:
        return image

    severity = np.float32(severity)
    a, b, c = np.asarray(SIMULATION[color_deficit], dtype=np.float32).T
    simulation = (a * (severity * severity) + b * severity + c).reshape(3, 3)

    identity = np.eye(3, dtype=np.float32)
    correction = identity.copy()
    axis = AXIS[color_deficit]
    correction[:, axis] = 0.7
    correction[axis, :] = 0
    matrix = identity + correction - correction @ simulation

    pixels = np.asarray(image, dtype=np.float32)
    result = pixels @ matrix.T
    np.clip(result, 0, 255, out=result)
    np.rint(result, out=result)
    return Image.fromarray(result.astype(np.uint8))