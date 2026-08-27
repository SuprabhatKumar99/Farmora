from pathlib import Path
import pandas as pd


class PreventionIPMPreprocessor:
    """Generic input loading for Expert 6.

    This layer does not invent prevention rules, IPM actions, thresholds,
    pesticide choices, or causal relationships. Those must come from the
    verified knowledge base/model contract.
    """

    SUPPORTED_EXTENSIONS = {".csv", ".parquet", ".json"}

    def load(self, input_path: str | Path) -> pd.DataFrame:
        path = Path(input_path)

        if not path.exists():
            raise FileNotFoundError(str(path))

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError("Unsupported Expert 6 input format.")

        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
        elif path.suffix.lower() == ".parquet":
            df = pd.read_parquet(path)
        else:
            df = pd.read_json(path)

        if df.empty:
            raise ValueError("EMPTY_INPUT")

        return df
