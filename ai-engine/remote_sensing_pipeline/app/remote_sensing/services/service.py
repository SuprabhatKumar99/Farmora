from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.remote_sensing.ingestion.raster import RasterIngestor
from app.remote_sensing.schemas.models import (
    RemoteSensingAsset,
    RemoteSensingProductType,
    RemoteSensingSource,
)
from app.remote_sensing.storage.local import LocalRemoteSensingStorage


class RemoteSensingService:
    def __init__(self, storage=None, ingestor=None):
        self.storage = storage
        self.ingestor = ingestor or RasterIngestor()
        self.assets = {}

    def register_asset(
        self,
        source_path: str | Path,
        source: RemoteSensingSource,
        product_type: RemoteSensingProductType,
        farm_id: str | None = None,
        zone_id: str | None = None,
        acquisition_time: datetime | None = None,
    ) -> RemoteSensingAsset:
        metadata = self.ingestor.inspect(source_path)
        asset_id = f"RS-{uuid4().hex[:12]}"

        if self.storage:
            file_path = self.storage.save(
                source_path,
                asset_id,
                Path(source_path).name,
            )
        else:
            file_path = str(source_path)

        asset = RemoteSensingAsset(
            asset_id=asset_id,
            farm_id=farm_id,
            zone_id=zone_id,
            source=source,
            product_type=product_type,
            acquisition_time=(
                acquisition_time or datetime.now(timezone.utc)
            ),
            file_path=file_path,
            width=metadata["width"],
            height=metadata["height"],
            band_count=metadata["band_count"],
            crs=metadata["crs"],
            nodata=metadata["nodata"],
        )

        self.assets[asset_id] = asset
        return asset

    def get_asset(self, asset_id: str) -> RemoteSensingAsset:
        asset = self.assets.get(asset_id)

        if asset is None:
            raise KeyError(asset_id)

        return asset
