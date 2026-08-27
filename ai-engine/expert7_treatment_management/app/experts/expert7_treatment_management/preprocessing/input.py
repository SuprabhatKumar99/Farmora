from pathlib import Path
import pandas as pd


class TreatmentManagementPreprocessor:
    """Generic case-input loading.

    It deliberately does not invent treatment rules, product names, active
    ingredients, rates, intervals, or crop-specific instructions.
    """

    SUPPORTED_EXTENSIONS = {".csv", ".parquet", ".json"}

    def load(self, input_path: str | Path) -> pd.DataFrame:
        path = Path(input_path)

        if not path.exists():
            raise FileNotFoundError(str(path))

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError("Unsupported Expert 7 input format.")

        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
        elif path.suffix.lower() == ".parquet":
            df = pd.read_parquet(path)
        else:
            df = pd.read_json(path)

        if df.empty:
            raise ValueError("EMPTY_INPUT")

        return df
