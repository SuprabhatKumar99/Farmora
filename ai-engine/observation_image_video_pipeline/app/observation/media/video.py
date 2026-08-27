from pathlib import Path
import cv2


class VideoFrameExtractor:
    """Extract frames at a controlled interval.

    It intentionally does not force inference on every frame.
    """

    def extract(
        self,
        video_path: str | Path,
        output_dir: str | Path,
        frame_interval_seconds: float = 1.0,
        max_frames: int | None = None,
    ) -> list[str]:
        if frame_interval_seconds <= 0:
            raise ValueError("frame_interval_seconds must be > 0")

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        capture = cv2.VideoCapture(str(video_path))

        if not capture.isOpened():
            raise ValueError("Unable to open video.")

        fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)

        if fps <= 0:
            capture.release()
            raise ValueError("Video FPS is unavailable.")

        frame_step = max(1, round(fps * frame_interval_seconds))

        saved = []
        frame_index = 0

        while True:
            ok, frame = capture.read()

            if not ok:
                break

            if frame_index % frame_step == 0:
                output = output_dir / f"frame_{frame_index:08d}.jpg"

                if not cv2.imwrite(str(output), frame):
                    capture.release()
                    raise IOError(f"Could not write frame: {output}")

                saved.append(str(output))

                if max_frames is not None and len(saved) >= max_frames:
                    break

            frame_index += 1

        capture.release()
        return saved
