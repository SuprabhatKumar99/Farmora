from pathlib import Path
import shutil


class LocalMediaStorage:
    """Development storage.

    Production can replace this adapter with MinIO/S3 without changing
    the observation service interface.
    """

    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, source: str | Path, observation_id: str, filename: str) -> str:
        source = Path(source)
        destination_dir = self.base_dir / observation_id
        destination_dir.mkdir(parents=True, exist_ok=True)

        destination = destination_dir / Path(filename).name
        shutil.copy2(source, destination)

        return str(destination)

    def get(self, media_path: str) -> Path:
        path = Path(media_path)

        if not path.exists():
            raise FileNotFoundError(media_path)

        return path
