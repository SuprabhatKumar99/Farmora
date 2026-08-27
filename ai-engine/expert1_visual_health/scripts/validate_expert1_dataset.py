from pathlib import Path
import pandas as pd

base = Path(__file__).resolve().parents[1] / "data/crop_health_dataset/08_expert1_visual_health"
for filename in ["expert1_observations.csv", "expert1_labels.csv"]:
    path = base / filename
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"{filename} is empty")
print("Expert 1 dataset validation: PASS")
