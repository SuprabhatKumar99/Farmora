import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.expert8_core_ai.api.routes import service
from app.expert8_core_ai.models.loader import DecisionModelLoader

if len(sys.argv) != 3:
    raise SystemExit(
        "Usage: python scripts/test_expert8.py <model-dir> <evidence-context.json>"
    )

model = DecisionModelLoader().load_huggingface(
    sys.argv[1],
    name="user_provided_agricultural_decision_model",
    version="provided",
)

service.set_model(model)

payload = json.loads(
    Path(sys.argv[2]).read_text(encoding="utf-8")
)

case_id = payload["case_id"]
context = payload["evidence_context"]

result = service.decide(case_id, context)

print(json.dumps(result.model_dump(mode="json"), indent=2))
