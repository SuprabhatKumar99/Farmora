from pathlib import Path
import pandas as pd

base = (
    Path(__file__).resolve().parents[1]
    / "data/crop_health_dataset/13_expert6_prevention_ipm"
)

for filename in [
    "expert6_cases.csv",
    "expert6_actions.csv",
]:
    path = base / filename

    if not path.exists():
        raise FileNotFoundError(path)

    if pd.read_csv(path).empty:
        raise ValueError(f"{filename} is empty")

print("Expert 6 dataset validation: PASS")
