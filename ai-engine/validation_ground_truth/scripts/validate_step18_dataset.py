from pathlib import Path
import csv

base = (
    Path(__file__).resolve().parents[1]
    / "data/crop_health_dataset/18_validation_ground_truth"
)

for name in ["ground_truth_cases.csv", "validation_cases.csv"]:
    path = base / name
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if len(rows) < 2:
        raise ValueError(f"{name} is empty")

print("Step 18 dataset structure validation: PASS")
