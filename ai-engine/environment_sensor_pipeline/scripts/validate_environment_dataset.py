from pathlib import Path
import pandas as pd

base = (
    Path(__file__).resolve().parents[1]
    / "data/crop_health_dataset/05_environment"
)

required = [
    "sensors.csv",
    "sensor_readings.csv",
]

for filename in required:
    path = base / filename

    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(f"{filename} is empty")

print("Environment dataset validation: PASS")

for filename in required:
    df = pd.read_csv(base / filename)
    print(f"{filename}: {len(df)} records")
