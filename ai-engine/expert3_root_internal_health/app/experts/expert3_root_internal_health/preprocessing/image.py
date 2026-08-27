from pathlib import Path
import cv2
import numpy as np


class ImagePreprocessor:
    """Generic safe input handling for Expert 3.

    Root/internal-health model preprocessing is model-specific. This module
    therefore does not assume a resolution, normalization, color convention,
    or modality that has not been supplied.
    """

    SUPPORTED_EXTENSIONS = {
        ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"
    }

    def load(self, image_path: str | Path) -> np.ndarray:
        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(str(path))

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError("Unsupported image extension.")

        image = cv2.imread(str(path))

        if image is None:
            raise ValueError("IMAGE_DECODE_FAILED")

        if image.size == 0:
            raise ValueError("EMPTY_IMAGE")

        return image

    @staticmethod
    def quality(image: np.ndarray) -> str:
        if image is None or image.size == 0:
            return "INVALID"

        h, w = image.shape[:2]
        return "LOW" if min(h, w) < 64 else "ACCEPTABLE"
