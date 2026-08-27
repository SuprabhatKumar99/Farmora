from pathlib import Path
import shutil


class LocalRemoteSensingStorage:
    """Development storage adapter.

    Production may replace this with MinIO/S3/object storage without
    changing ingestion or analysis code.
    """

    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, source: str | Path, asset_id: str, filename: str) -> str:
        source = Path(source)
        target_dir = self.base_dir / asset_id
        target_dir.mkdir(parents=True, exist_ok=True)

        destination = target_dir / Path(filename).name
        shutil.copy2(source, destination)

        return str(destination)
