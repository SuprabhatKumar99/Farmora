from pathlib import Path
import csv

base = (
    Path(__file__).resolve().parents[1]
    / "data/crop_health_dataset/16_expert8_core_ai"
)

for name in ["decision_cases.csv", "decision_targets.csv"]:
    path = base / name
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8") as f:
        if len(list(csv.reader(f))) < 2:
            raise ValueError(f"{name} is empty")

print("Expert 8 dataset validation: PASS")
