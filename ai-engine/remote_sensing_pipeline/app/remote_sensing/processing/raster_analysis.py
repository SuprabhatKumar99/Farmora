from pathlib import Path

import rasterio

from app.remote_sensing.processing.indices import (
    ndmi,
    ndvi,
    ndwi,
    summarize_array,
)
from app.remote_sensing.schemas.models import RasterSummary, SpectralIndexResult


class RasterAnalyzer:
    """Basic raster analysis.

    Band numbers must be supplied by the caller because band ordering differs
    between remote-sensing products. This module never assumes that band 4,
    band 5, etc. mean a particular wavelength unless the caller specifies it.
    """

    def summarize(self, asset_id: str, path: str | Path) -> RasterSummary:
        with rasterio.open(path) as dataset:
            first = dataset.read(1, masked=True)

            valid = int((~first.mask).sum())
            total = int(first.size)

            return RasterSummary(
                asset_id=asset_id,
                width=dataset.width,
                height=dataset.height,
                band_count=dataset.count,
                crs=str(dataset.crs) if dataset.crs else None,
                nodata=dataset.nodata,
                valid_pixels=valid,
                total_pixels=total,
            )

    def calculate_ndvi(
        self,
        asset_id: str,
        path: str | Path,
        nir_band: int,
        red_band: int,
    ) -> SpectralIndexResult:
        with rasterio.open(path) as dataset:
            nir = dataset.read(nir_band, masked=True)
            red = dataset.read(red_band, masked=True)

        result = ndvi(nir, red)
        return SpectralIndexResult(**summarize_array("NDVI", result))

    def calculate_ndwi(
        self,
        asset_id: str,
        path: str | Path,
        nir_band: int,
        green_band: int,
    ) -> SpectralIndexResult:
        with rasterio.open(path) as dataset:
            nir = dataset.read(nir_band, masked=True)
            green = dataset.read(green_band, masked=True)

        result = ndwi(nir, green)
        return SpectralIndexResult(**summarize_array("NDWI", result))

    def calculate_ndmi(
        self,
        asset_id: str,
        path: str | Path,
        nir_band: int,
        swir_band: int,
    ) -> SpectralIndexResult:
        with rasterio.open(path) as dataset:
            nir = dataset.read(nir_band, masked=True)
            swir = dataset.read(swir_band, masked=True)

        result = ndmi(nir, swir)
        return SpectralIndexResult(**summarize_array("NDMI", result))
