from pathlib import Path
import pandas as pd

class CropKnowledgeRepository:
    def __init__(self, base_path: str | Path):
        self.base_path = Path(base_path)
        self.crops = self._load("crops.csv")
        self.varieties = self._load("varieties.csv")
        self.growth_stages = self._load("growth_stages.csv")
        self.crop_lifecycle = self._load("crop_lifecycle.csv")
        self.crop_requirements = self._load("crop_requirements.csv")

    def _load(self, filename):
        path = self.base_path / filename
        if not path.exists():
            raise FileNotFoundError(f"Knowledge dataset not found: {path}")
        return pd.read_csv(path)

    def get_crop(self, crop_id):
        result = self.crops[self.crops["crop_id"].astype(str) == str(crop_id)]
        return None if result.empty else result.iloc[0].to_dict()

    def get_varieties(self, crop_id):
        result = self.varieties[self.varieties["crop_id"].astype(str) == str(crop_id)]
        return result.to_dict(orient="records")

    def get_growth_stages(self, crop_id):
        result = self.growth_stages[self.growth_stages["crop_id"].astype(str) == str(crop_id)]
        return result.to_dict(orient="records")

    def get_crop_lifecycle(self, crop_id):
        if "crop_id" not in self.crop_lifecycle.columns:
            return self.crop_lifecycle.to_dict(orient="records")
        result = self.crop_lifecycle[self.crop_lifecycle["crop_id"].astype(str) == str(crop_id)]
        return result.to_dict(orient="records")

    def get_requirements(self, crop_id, variety_id=None):
        result = self.crop_requirements[
            self.crop_requirements["crop_id"].astype(str) == str(crop_id)
        ]
        if variety_id is not None and "variety_id" in result.columns:
            result = result[result["variety_id"].astype(str) == str(variety_id)]
        return result.to_dict(orient="records")

    def list_crop_ids(self):
        return sorted(self.crops["crop_id"].dropna().astype(str).unique().tolist())
