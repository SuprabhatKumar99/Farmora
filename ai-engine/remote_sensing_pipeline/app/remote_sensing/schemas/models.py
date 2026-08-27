from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class RemoteSensingSource(str, Enum):
    DRONE = "DRONE"
    SATELLITE = "SATELLITE"


class RemoteSensingProductType(str, Enum):
    MULTISPECTRAL = "MULTISPECTRAL"
    RGB = "RGB"
    THERMAL = "THERMAL"
    UNKNOWN = "UNKNOWN"


class RemoteSensingAsset(BaseModel):
    asset_id: str
    farm_id: str | None = None
    zone_id: str | None = None
    source: RemoteSensingSource
    product_type: RemoteSensingProductType
    acquisition_time: datetime
    file_path: str
    width: int | None = Field(default=None, ge=0)
    height: int | None = Field(default=None, ge=0)
    band_count: int | None = Field(default=None, ge=0)
    crs: str | None = None
    nodata: float | None = None


class SpectralIndexResult(BaseModel):
    index_name: str
    value: float | None = None
    valid_pixels: int = Field(ge=0)
    total_pixels: int = Field(ge=0)


class RasterSummary(BaseModel):
    asset_id: str
    width: int
    height: int
    band_count: int
    crs: str | None = None
    nodata: float | None = None
    valid_pixels: int = Field(ge=0)
    total_pixels: int = Field(ge=0)
    indices: list[SpectralIndexResult] = Field(default_factory=list)
