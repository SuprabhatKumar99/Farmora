from pathlib import Path
import pandas as pd

base = (
    Path(__file__).resolve().parents[1]
    / "data/crop_health_dataset/10_expert3_root_internal_health"
)

for filename in [
    "expert3_observations.csv",
    "expert3_labels.csv",
]:
    path = base / filename

    if not path.exists():
        raise FileNotFoundError(path)

    if pd.read_csv(path).empty:
        raise ValueError(f"{filename} is empty")

print("Expert 3 dataset validation: PASS")
