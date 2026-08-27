import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.observation.media.validator import MediaValidator

if len(sys.argv) != 2:
    raise SystemExit("Usage: python scripts/test_image.py <image-path>")

path = Path(sys.argv[1])
result = MediaValidator().validate(path, "image/" + path.suffix.lstrip(".") if path.suffix else "application/octet-stream")

print(result.model_dump())
