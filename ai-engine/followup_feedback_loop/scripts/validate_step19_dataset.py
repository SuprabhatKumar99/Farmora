from pathlib import Path
import csv

base = (
    Path(__file__).resolve().parents[1]
    / "data/crop_health_dataset/19_followup_feedback_loop"
)

for name in ["followup_cases.csv", "feedback_records.csv"]:
    path = base / name
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8") as f:
        if len(list(csv.reader(f))) < 2:
            raise ValueError(f"{name} is empty")

print("Step 19 dataset structure validation: PASS")
