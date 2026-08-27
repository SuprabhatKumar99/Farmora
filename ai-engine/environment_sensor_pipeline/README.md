# STEP 5 — Environment & Sensor Pipeline

This package implements **only Step 5** of the AI Engine roadmap.

It preserves the existing project structure and adds the Step 5 environment layer.

## Dataset structure

```text
crop_health_dataset/
├── 01_crop_knowledge/
├── 02_disease_pest_knowledge/
├── 03_farm/
├── 04_observations/
└── 05_environment/
    ├── sensors.csv
    └── sensor_readings.csv
```

The new Step 5 files are:

```text
05_environment/
├── sensors.csv
└── sensor_readings.csv
```

No previous dataset directory is renamed, removed, or modified.

## Why these application layers are required

The environment pipeline needs a separation between:

```text
Sensor registration
       ↓
Ingestion
       ↓
Validation / quality checks
       ↓
Normalized reading
       ↓
Aggregation
       ↓
Later farm analytics
```

The application implementation therefore adds:

```text
app/environment/
├── api/
├── schemas/
├── services/
├── ingestion/
├── processing/
└── storage/
```

## Implemented

- Sensor model
- Sensor reading model
- Sensor registration
- Sensor reading ingestion
- Farm/zone association
- Timestamp handling
- Basic physical plausibility validation
- Rejection status for invalid readings
- Time-window aggregation component
- In-memory development storage
- FastAPI endpoints
- Tests
- Dataset validation script

## Important boundary

The quality ranges in `processing/quality.py` are **data-validation guardrails only**.

They are not:
- disease thresholds
- crop-specific recommendations
- treatment thresholds
- agronomic prescriptions

Do not use them as agricultural decision rules.

Crop-specific environmental conditions belong to the Crop Knowledge Base and later farm-risk/condition logic.

## Sensor types supported

```text
SOIL_MOISTURE
TEMPERATURE
HUMIDITY
RAINFALL
LIGHT
LEAF_WETNESS
OTHER
```

The `OTHER` type allows future sensor integration without changing the core model.

## Reading lifecycle

```text
Incoming reading
      ↓
Sensor lookup
      ↓
Value validation
      ↓
Timestamp validation
      ↓
ACCEPTED / REJECTED
      ↓
Store normalized reading
```

A rejected reading is retained with `REJECTED` status so that the pipeline does not silently discard bad sensor data.

## API

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health:

```text
GET /health
GET /ready
```

Register sensor:

```text
POST /api/v1/environment/sensors
```

Example:

```json
{
  "sensor_id": "S001",
  "farm_id": "F001",
  "zone_id": "Z001",
  "sensor_type": "SOIL_MOISTURE",
  "unit": "%",
  "latitude": 26.7271,
  "longitude": 88.3953,
  "active": true
}
```

Ingest reading:

```text
POST /api/v1/environment/readings
```

Example:

```json
{
  "sensor_id": "S001",
  "value": 45.0,
  "recorded_at": "2026-08-27T09:00:00Z"
}
```

Readings:

```text
GET /api/v1/environment/readings
```

## Dataset testing

```bash
python scripts/validate_environment_dataset.py
```

## Unit tests

```bash
pytest -q
```

## Aggregation

`SensorAggregator` provides descriptive time-window statistics:

```text
count
mean
min
max
std
```

It does not calculate disease risk.

Example concept:

```text
raw sensor readings
       ↓
hourly window
       ↓
mean/min/max/std
```

This prepares clean temporal environmental features for later analytics.

## Storage

Development uses:

```text
InMemorySensorStore
```

This is intentional so Step 5 can be tested independently.

For the full architecture, the storage adapter can later be replaced with the project's backend persistence layer, while keeping the service interface stable.

For production high-frequency time-series workloads, a dedicated time-series persistence strategy can be introduced without changing the sensor models or quality-processing contract.

## Kafka boundary

Kafka is intentionally **not required for the standalone Step 5 package**.

In the full architecture, the integration should be:

```text
IoT / Sensor Gateway
        ↓
Spring Boot / Kafka
        ↓
Environment AI Engine
        ↓
Validation / Processing
        ↓
Kafka environment event
        ↓
Farm Analytics
```

The current package keeps the processing logic independent so Kafka can be integrated without coupling the core quality logic to a broker.

## AI Engine boundary

Step 5 does not implement:

- disease prediction
- pest prediction
- zone risk scoring
- vegetation analysis
- image inference
- Expert 1–7
- Expert 8
- evidence fusion
- treatment recommendations

It produces validated environmental observations for subsequent stages.

## Testing with real sensor data

Replace:

```text
data/crop_health_dataset/05_environment/sensors.csv
data/crop_health_dataset/05_environment/sensor_readings.csv
```

with the actual verified records while keeping the same filenames and directory.

Then run:

```bash
python scripts/validate_environment_dataset.py
pytest -q
```

For real deployment, sensor-specific units and validation limits should be defined from the actual sensor specifications and dataset—not assumed by the AI engine.
