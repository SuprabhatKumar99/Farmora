import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.experts.expert7_treatment_management.api.routes import get_service
from app.experts.expert7_treatment_management.models.loader import (
    TreatmentManagementModelLoader,
)

if len(sys.argv) != 3:
    raise SystemExit(
        "Usage: python scripts/test_expert7.py <torchscript-model> <case.csv>"
    )

service = get_service()

model = TreatmentManagementModelLoader().load_torchscript(
    sys.argv[1],
    name="user_provided_treatment_management_model",
    version="provided",
    task="RECOMMENDATION",
)

service.set_model(model)

result = service.analyze(
    case_id="LOCAL-TEST",
    input_path=sys.argv[2],
)

print(result.model_dump(mode="json"))
