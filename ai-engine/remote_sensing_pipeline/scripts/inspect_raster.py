import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.remote_sensing.ingestion.raster import RasterIngestor

if len(sys.argv) != 2:
    raise SystemExit("Usage: python scripts/inspect_raster.py <geotiff>")

path = Path(sys.argv[1])
print(RasterIngestor().inspect(path))
