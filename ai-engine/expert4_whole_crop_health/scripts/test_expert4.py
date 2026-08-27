import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.experts.expert4_whole_crop_health.api.routes import get_service
from app.experts.expert4_whole_crop_health.models.loader import (
    WholeCropHealthModelLoader,
)

if len(sys.argv) != 3:
    raise SystemExit(
        "Usage: python scripts/test_expert4.py <torchscript-model> <image>"
    )

service = get_service()

model = WholeCropHealthModelLoader().load_torchscript(
    sys.argv[1],
    name="user_provided_whole_crop_health_model",
    version="provided",
    task="DETECTION",
)

service.set_model(model)

result = service.analyze(
    observation_id="LOCAL-TEST",
    image_path=sys.argv[2],
)

print(result.model_dump(mode="json"))
