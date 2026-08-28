from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

def main():
    meta_path = ROOT / "04_observations/image_metadata.csv"
    out = ROOT / "expert_1_visual_health/reports"
    out.mkdir(parents=True, exist_ok=True)
    if not meta_path.exists():
        print(f"Metadata not found: {meta_path}")
        print("Place the canonical image_metadata.csv in 04_observations/ and rerun.")
        return
    df = pd.read_csv(meta_path)
    required = ["image_id","file_path","farm_id","zone_id","crop_id","growth_stage"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required metadata columns: {missing}")
    df["file_exists"] = df["file_path"].map(lambda p: (ROOT / "04_observations" / str(p)).exists())
    df.to_csv(out / "dataset_audit.csv", index=False)
    print(f"Rows: {len(df)}")
    print(f"Missing files: {(~df.file_exists).sum()}")
    print(f"Audit: {out/'dataset_audit.csv'}")

if __name__ == "__main__":
    main()
