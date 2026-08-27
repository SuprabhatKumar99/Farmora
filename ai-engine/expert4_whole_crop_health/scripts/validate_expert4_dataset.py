from pathlib import Path
import pandas as pd

base = (
    Path(__file__).resolve().parents[1]
    / "data/crop_health_dataset/11_expert4_whole_crop_health"
)

for filename in [
    "expert4_observations.csv",
    "expert4_labels.csv",
]:
    path = base / filename

    if not path.exists():
        raise FileNotFoundError(path)

    if pd.read_csv(path).empty:
        raise ValueError(f"{filename} is empty")

print("Expert 4 dataset validation: PASS")
