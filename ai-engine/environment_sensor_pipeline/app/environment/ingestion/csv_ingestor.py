from pathlib import Path
import pandas as pd


class SensorCsvIngestor:
    """Loads sensor readings from CSV without changing the dataset files."""

    def load(self, path: str | Path) -> pd.DataFrame:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        return pd.read_csv(path)
