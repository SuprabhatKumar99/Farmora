import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.experts.expert1_visual_health.api.routes import get_service
from app.experts.expert1_visual_health.models.loader import VisualModelLoader

if len(sys.argv) != 3:
    raise SystemExit("Usage: python scripts/test_expert1.py <torchscript-model> <image>")

service = get_service()
model = VisualModelLoader().load_torchscript(
    sys.argv[1],
    name="user_provided_visual_health_model",
    version="provided",
    task="DETECTION"
)
service.set_model(model)
print(service.analyze("LOCAL-TEST", sys.argv[2]).model_dump(mode="json"))
