from pathlib import Path
import rasterio


class RasterIngestor:
    """Reads raster metadata and bands.

    The ingestor does not change the source raster.
    """

    SUPPORTED_EXTENSIONS = {".tif", ".tiff"}

    def inspect(self, path: str | Path) -> dict:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError("Only GeoTIFF raster files are supported by this step.")

        with rasterio.open(path) as dataset:
            return {
                "width": dataset.width,
                "height": dataset.height,
                "band_count": dataset.count,
                "crs": str(dataset.crs) if dataset.crs else None,
                "nodata": dataset.nodata,
                "dtype": dataset.dtypes,
                "bounds": tuple(dataset.bounds),
                "transform": dataset.transform,
            }

    def read_band(self, path: str | Path, band_number: int):
        path = Path(path)

        with rasterio.open(path) as dataset:
            if band_number < 1 or band_number > dataset.count:
                raise ValueError(
                    f"band_number must be between 1 and {dataset.count}"
                )

            return dataset.read(band_number, masked=True)
