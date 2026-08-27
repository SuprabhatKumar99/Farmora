from pathlib import Path
import pandas as pd

base = (
    Path(__file__).resolve().parents[1]
    / "data/crop_health_dataset/14_expert7_treatment_management"
)

for filename in [
    "expert7_cases.csv",
    "expert7_treatments.csv",
]:
    path = base / filename

    if not path.exists():
        raise FileNotFoundError(path)

    if pd.read_csv(path).empty:
        raise ValueError(f"{filename} is empty")

print("Expert 7 dataset validation: PASS")
