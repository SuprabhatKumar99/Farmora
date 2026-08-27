from pathlib import Path
import csv

base = (
    Path(__file__).resolve().parents[1]
    / "data/crop_health_dataset/17_decision_risk_recommendation_outputs"
)

for name in [
    "decision_outputs_cases.csv",
    "recommendation_outputs.csv",
]:
    path = base / name
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8") as f:
        if len(list(csv.reader(f))) < 2:
            raise ValueError(f"{name} is empty")

print("Step 17 dataset validation: PASS")
