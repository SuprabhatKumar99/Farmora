# STEP 6 — Remote Sensing Pipeline

This package implements **only Step 6** of the AI Engine roadmap.

The existing project structure is preserved and Step 6 is added as a separate remote-sensing module.

## Dataset structure

```text
crop_health_dataset/
├── 01_crop_knowledge/
├── 02_disease_pest_knowledge/
├── 03_farm/
├── 04_observations/
├── 05_environment/
└── 06_remote_sensing/
    ├── remote_sensing_assets.csv
    └── remote_sensing_metadata.csv
```

No previous dataset directory is renamed, removed, merged, or replaced.

## Added application structure

```text
app/remote_sensing/
├── api/
├── schemas/
├── ingestion/
├── processing/
├── services/
└── storage/
```

These layers are required to keep raster ingestion, numerical processing, service orchestration, and storage separate.

## Implemented

- Remote-sensing asset model
- Raster/GeoTIFF inspection
- Raster metadata extraction
- Band reading
- NDVI calculation
- NDWI calculation
- NDMI calculation
- Masked invalid-value handling
- Raster summary
- Farm/zone association
- Local object-storage adapter
- FastAPI health/readiness endpoint
- Tests
- Raster inspection script
- Index testing script

## Important: band ordering is NOT assumed

Different satellite/drone products can use different band ordering.

Therefore the implementation requires the caller to explicitly provide:

```text
NIR band
Red band
Green band
SWIR band
```

when calculating indices.

The code does not assume that a particular numeric band is NIR, Red, Green, or SWIR.

This avoids silently producing incorrect indices.

## Mathematical definitions

### NDVI

```text
NDVI = (NIR - Red) / (NIR + Red)
```

### NDWI

This implementation uses the NIR/Green normalized-difference variant:

```text
NDWI = (Green - NIR) / (Green + NIR)
```

### NDMI

```text
NDMI = (NIR - SWIR) / (NIR + SWIR)
```

If the denominator is zero, the result is masked rather than producing an invalid infinite value.

## Processing flow

```text
Drone / Satellite Raster
          ↓
GeoTIFF Inspection
          ↓
Metadata Extraction
          ↓
Band Selection
          ↓
Raster Reading
          ↓
Spectral Index Calculation
          ↓
Masked / Valid Pixel Handling
          ↓
Summary Features
          ↓
Farm Analytics
```

## Why this step does not create disease decisions

Remote-sensing indices are features/observations.

This step does NOT claim:

```text
low NDVI = disease
high NDVI = healthy
```

by itself.

Such conclusions require crop-specific context, temporal comparison, zone-level analysis, environmental conditions, and the expert models defined in later stages.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

## Test

```bash
pytest -q
```

## Test the mathematical index implementation

```bash
python scripts/test_indices.py
```

## Inspect a real GeoTIFF

```bash
python scripts/inspect_raster.py path/to/remote_sensing.tif
```

The script reports:

```text
width
height
band_count
CRS
nodata
dtype
bounds
transform
```

## Raster requirements

The current ingestion implementation accepts:

```text
.tif
.tiff
```

GeoTIFF is used because the pipeline needs raster dimensions, bands, geospatial reference information, and nodata handling.

## Storage

Development uses:

```text
LocalRemoteSensingStorage
```

Production can replace this adapter with:

```text
MinIO / S3
```

The raster itself should remain in object storage rather than being embedded inside Kafka messages.

Kafka events should later carry an asset identifier/object-storage reference and relevant metadata.

## Full architecture integration

The eventual pipeline is:

```text
Drone / Satellite
       ↓
Object Storage
       ↓
Remote Sensing Pipeline
       ↓
Raster Processing
       ↓
NDVI / NDWI / NDMI / other verified features
       ↓
Farm / Zone Analytics
       ↓
Zone Risk Map
       ↓
Detailed inspection
       ↓
Experts 1–7
```

This step therefore produces remote-sensing features for the later Farm Analytics Engine.

## Important boundary

Step 6 does NOT implement:

- farm segmentation
- vegetation anomaly detection
- temporal change detection
- zone risk scoring
- disease diagnosis
- pest diagnosis
- Expert 1–7
- Expert 8
- evidence fusion
- treatment recommendation
- Kafka integration
- PostgreSQL integration

Those belong to subsequent stages.

## Dataset rule

The example CSV files are minimal executable placeholders.

Use the actual verified remote-sensing records while keeping:

```text
06_remote_sensing/
├── remote_sensing_assets.csv
└── remote_sensing_metadata.csv
```

If your actual supplied Step 6 dataset contains additional files, keep those files in the same directory. Do not rename them to fit this example.

## No fabricated agricultural thresholds

This implementation intentionally does not define disease thresholds, crop-health thresholds, or intervention thresholds for NDVI/NDWI/NDMI.

Those thresholds must be established from verified crop-specific data and the project's later analytics methodology rather than assumed here.
