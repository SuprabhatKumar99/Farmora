from pathlib import Path
import pandas as pd


class FarmDigitalProfileRepository:
    # The dataset structure is preserved exactly:
    # 03_farm/
    # ├── farms.csv
    # ├── fields.csv
    # ├── zones.csv
    # └── crop_cycles.csv

    FILES = (
        "farms.csv",
        "fields.csv",
        "zones.csv",
        "crop_cycles.csv",
    )

    def __init__(self, base_path: str | Path):
        self.base_path = Path(base_path)

        if not self.base_path.exists():
            raise FileNotFoundError(
                f"Farm dataset directory not found: {self.base_path}"
            )

        self.farms = self._load("farms.csv")
        self.fields = self._load("fields.csv")
        self.zones = self._load("zones.csv")
        self.crop_cycles = self._load("crop_cycles.csv")

    def _load(self, filename: str) -> pd.DataFrame:
        path = self.base_path / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Farm dataset not found: {path}"
            )

        return pd.read_csv(path)

    @staticmethod
    def _filter(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
        if column not in df.columns:
            return df.iloc[0:0]

        return df[df[column].astype(str) == str(value)]

    def get_farm(self, farm_id: str) -> dict | None:
        result = self._filter(self.farms, "farm_id", farm_id)

        if result.empty:
            return None

        return result.iloc[0].to_dict()

    def get_fields(self, farm_id: str) -> list[dict]:
        return self._filter(
            self.fields, "farm_id", farm_id
        ).to_dict(orient="records")

    def get_zones(self, farm_id: str) -> list[dict]:
        return self._filter(
            self.zones, "farm_id", farm_id
        ).to_dict(orient="records")

    def get_crop_cycles(self, farm_id: str) -> list[dict]:
        return self._filter(
            self.crop_cycles, "farm_id", farm_id
        ).to_dict(orient="records")

    def get_crop_cycles_for_zone(self, zone_id: str) -> list[dict]:
        return self._filter(
            self.crop_cycles, "zone_id", zone_id
        ).to_dict(orient="records")

    def get_zone(self, zone_id: str) -> dict | None:
        result = self._filter(self.zones, "zone_id", zone_id)

        if result.empty:
            return None

        return result.iloc[0].to_dict()
