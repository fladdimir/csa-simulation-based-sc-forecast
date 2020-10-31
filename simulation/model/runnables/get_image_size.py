from typing import Tuple

from PIL import Image


def get_size(path: str) -> Tuple[int, int]:
    im = Image.open(path)
    return im.size  # width, height
