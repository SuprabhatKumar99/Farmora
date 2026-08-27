import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.observation.media.video import VideoFrameExtractor

if len(sys.argv) < 2:
    raise SystemExit(
        "Usage: python scripts/extract_video_frames.py <video-path> [interval-seconds]"
    )

video = Path(sys.argv[1])
interval = float(sys.argv[2]) if len(sys.argv) >= 3 else 1.0

output = Path("data/media/frames") / video.stem

frames = VideoFrameExtractor().extract(
    video_path=video,
    output_dir=output,
    frame_interval_seconds=interval,
)

print(f"Extracted {len(frames)} frames")
print(f"Output: {output}")
