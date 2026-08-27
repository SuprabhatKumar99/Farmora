from pathlib import Path
import pandas as pd
class EnvironmentPreprocessor:
    SUPPORTED_EXTENSIONS={'.csv','.parquet','.json'}
    def load(self,path):
        p=Path(path)
        if not p.exists(): raise FileNotFoundError(str(p))
        if p.suffix.lower() not in self.SUPPORTED_EXTENSIONS: raise ValueError('Unsupported environment/weather data format.')
        df = pd.read_csv(p) if p.suffix.lower()=='.csv' else pd.read_parquet(p) if p.suffix.lower()=='.parquet' else pd.read_json(p)
        if df.empty: raise ValueError('EMPTY_DATASET')
        return df
    def validate_timestamp(self,df):
        if 'timestamp' not in df.columns: raise ValueError('TIMESTAMP_COLUMN_MISSING')
        x=pd.to_datetime(df['timestamp'],errors='coerce')
        if x.isna().all(): raise ValueError('INVALID_TIMESTAMP_COLUMN')
        return x
