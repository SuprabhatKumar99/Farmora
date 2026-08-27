from pathlib import Path
import cv2

from app.observation.schemas.models import (
    MediaValidationResult,
    ObservationType,
)


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".m4v"}


class MediaValidator:
    def __init__(self, max_image_bytes=20 * 1024 * 1024,
                 max_video_bytes=500 * 1024 * 1024):
        self.max_image_bytes = max_image_bytes
        self.max_video_bytes = max_video_bytes

    def validate(self, path: str | Path, content_type: str) -> MediaValidationResult:
        path = Path(path)

        if not path.exists() or not path.is_file():
            return MediaValidationResult(
                valid=False,
                content_type=content_type,
                size_bytes=0,
                error_code="MEDIA_NOT_FOUND",
                error_message="Media file does not exist.",
            )

        size = path.stat().st_size
        ext = path.suffix.lower()

        media_type = self._media_type(ext, content_type)

        if media_type is None:
            return MediaValidationResult(
                valid=False,
                content_type=content_type,
                size_bytes=size,
                error_code="UNSUPPORTED_MEDIA_TYPE",
                error_message="Unsupported image or video format.",
            )

        max_size = (
            self.max_image_bytes
            if media_type == ObservationType.IMAGE
            else self.max_video_bytes
        )

        if size > max_size:
            return MediaValidationResult(
                valid=False,
                media_type=media_type,
                content_type=content_type,
                size_bytes=size,
                error_code="MEDIA_TOO_LARGE",
                error_message="Media exceeds the configured size limit.",
            )

        if media_type == ObservationType.IMAGE:
            return self._validate_image(path, content_type, size)

        return self._validate_video(path, content_type, size)

    @staticmethod
    def _media_type(ext, content_type):
        if ext in IMAGE_EXTENSIONS or content_type.startswith("image/"):
            return ObservationType.IMAGE
        if ext in VIDEO_EXTENSIONS or content_type.startswith("video/"):
            return ObservationType.VIDEO
        return None

    @staticmethod
    def _validate_image(path, content_type, size):
        image = cv2.imread(str(path))

        if image is None:
            return MediaValidationResult(
                valid=False,
                media_type=ObservationType.IMAGE,
                content_type=content_type,
                size_bytes=size,
                error_code="IMAGE_DECODE_FAILED",
                error_message="Image could not be decoded.",
            )

        height, width = image.shape[:2]

        return MediaValidationResult(
            valid=True,
            media_type=ObservationType.IMAGE,
            content_type=content_type,
            size_bytes=size,
            width=width,
            height=height,
        )

    @staticmethod
    def _validate_video(path, content_type, size):
        capture = cv2.VideoCapture(str(path))

        if not capture.isOpened():
            return MediaValidationResult(
                valid=False,
                media_type=ObservationType.VIDEO,
                content_type=content_type,
                size_bytes=size,
                error_code="VIDEO_DECODE_FAILED",
                error_message="Video could not be opened.",
            )

        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)

        duration = None
        if fps > 0 and frame_count >= 0:
            duration = frame_count / fps

        ok, _ = capture.read()
        capture.release()

        if not ok:
            return MediaValidationResult(
                valid=False,
                media_type=ObservationType.VIDEO,
                content_type=content_type,
                size_bytes=size,
                width=width,
                height=height,
                frame_count=frame_count,
                fps=fps,
                duration_seconds=duration,
                error_code="VIDEO_FRAME_READ_FAILED",
                error_message="No readable video frame was found.",
            )

        return MediaValidationResult(
            valid=True,
            media_type=ObservationType.VIDEO,
            content_type=content_type,
            size_bytes=size,
            width=width,
            height=height,
            frame_count=frame_count,
            fps=fps,
            duration_seconds=duration,
        )
