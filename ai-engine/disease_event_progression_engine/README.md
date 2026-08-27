# STEP 7 — Disease Event & Progression Engine

This package implements **only Step 7** of the AI Engine roadmap.

It adds disease/pest event tracking and temporal progression without changing the existing project structure.

## Dataset structure

```text
crop_health_dataset/
├── 01_crop_knowledge/
├── 02_disease_pest_knowledge/
├── 03_farm/
├── 04_observations/
├── 05_environment/
├── 06_remote_sensing/
└── 07_disease_events/
    ├── disease_events.csv
    ├── disease_event_evidence.csv
    └── progression_observations.csv
```

No previous dataset directory is renamed, removed, merged, or replaced.

The Step 7 directory is additive.

## Application structure

```text
app/disease_events/
├── api/
├── schemas/
├── services/
├── processing/
└── storage/
```

## Purpose

Step 7 creates a temporal record that connects observations/evidence to a farm zone.

Conceptually:

```text
Image / Video
Sensor data
Remote sensing
Farmer report
Laboratory result
Expert result
       ↓
Disease/Pest Event
       ↓
Evidence
       ↓
Repeated observations
       ↓
Progression timeline
```

The engine does not independently diagnose disease.

## Implemented

- Disease event model
- Evidence model
- Progression observation model
- Event lifecycle/status
- Evidence references
- Temporal validation
- Severity representation from 0 to 1
- Progression analysis
- Increasing/decreasing/stable detection
- Elapsed-time calculation
- Timeline aggregation
- In-memory development storage
- FastAPI endpoints
- Tests
- Dataset validation script

## Event lifecycle

The model supports:

```text
OBSERVED
SUSPECTED
CONFIRMED
RESOLVED
```

These are states recorded by the wider system. This step does not automatically decide that an event is confirmed.

## Evidence types

```text
IMAGE
VIDEO
SENSOR
REMOTE_SENSING
FARMER_REPORT
LABORATORY
EXPERT
```

Each evidence record points to an external reference:

```text
reference_id
```

For example, an IMAGE evidence record can point to an observation ID from Step 4.

A REMOTE_SENSING record can point to an asset from Step 6.

A SENSOR record can point to an environment reading/event from Step 5.

## Progression representation

Severity is represented on a normalized scale:

```text
0.0 → 1.0
```

This is a data representation, not a claim that every crop/disease uses the same agronomic severity definition.

The later disease-specific model should define how severity is estimated.

## Progression mathematics

For two consecutive severity observations:

```text
ΔS = S_current - S_previous
```

where:

```text
S_previous = previous severity
S_current  = current severity
```

Direction:

```text
ΔS > 0  → INCREASING
ΔS = 0  → STABLE
ΔS < 0  → DECREASING
```

Elapsed time:

```text
Δt = t_current - t_previous
```

converted to hours.

The current implementation intentionally does not invent a biological growth-rate model.

If a rate is needed later, it can be expressed as:

```text
severity_change_rate = ΔS / Δt
```

but this step does not treat that rate as a disease-specific biological parameter.

## Processing flow

```text
Disease/Pest Event
       ↓
Evidence Collection
       ↓
Progression Observations
       ↓
Temporal Ordering
       ↓
Severity Comparison
       ↓
ΔS and Δt
       ↓
Increasing / Stable / Decreasing
       ↓
Progression Result
```

## Important temporal rule

A progression observation must lie inside the event's recorded observation window:

```text
first_observed_at
        ≤
observation.observed_at
        ≤
last_observed_at
```

This prevents the engine from silently accepting observations outside the event timeline.

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

Create event:

```text
POST /api/v1/disease-events
```

Example:

```json
{
  "farm_id": "F001",
  "zone_id": "Z001",
  "crop_id": "C001",
  "variety_id": "V001",
  "disease_id": "D001",
  "first_observed_at": "2026-08-27T09:00:00Z",
  "status": "OBSERVED",
  "severity": 0.25
}
```

Add evidence:

```text
POST /api/v1/disease-events/{event_id}/evidence
```

Example:

```json
{
  "evidence_type": "IMAGE",
  "reference_id": "OBS-001",
  "observed_at": "2026-08-27T09:00:00Z",
  "confidence": 0.90,
  "notes": "Image observation"
}
```

Add progression observation:

```text
POST /api/v1/disease-events/{event_id}/progression
```

Example:

```json
{
  "observed_at": "2026-08-27T09:00:00Z",
  "severity": 0.25,
  "evidence_ids": ["EVD-001"]
}
```

Analyze progression:

```text
GET /api/v1/disease-events/{event_id}/progression
```

Timeline:

```text
GET /api/v1/disease-events/{event_id}/timeline
```

## Testing

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run:

```bash
pytest -q
```

Validate the dataset:

```bash
python scripts/validate_disease_events_dataset.py
```

## Storage boundary

The package uses:

```text
InMemoryDiseaseEventStore
```

for standalone testing.

In the complete architecture, event persistence belongs to the backend/persistence layer. The AI engine should not directly couple this component to PostgreSQL.

The storage adapter can later be replaced without changing the progression algorithm.

## Relationship to previous steps

```text
STEP 3
Farm Digital Profile
        ↓
farm_id / zone_id

STEP 4
Observation Pipeline
        ↓
observation_id

STEP 5
Environment & Sensor Pipeline
        ↓
sensor evidence

STEP 6
Remote Sensing Pipeline
        ↓
remote-sensing asset evidence

STEP 7
Disease Event & Progression
        ↓
temporal disease/pest event context
```

## Important boundary

Step 7 does NOT implement:

- disease diagnosis
- pest diagnosis
- YOLO
- image classification
- disease-specific severity models
- farm risk scoring
- Expert 1–7
- Expert 8
- evidence fusion
- treatment recommendation
- IPM recommendation
- Kafka
- PostgreSQL
- LLM inference

Those belong to later stages.

## No hallucinated disease progression rules

This implementation deliberately does not claim:

```text
Disease X progresses at Y/day
Disease X becomes severe above Z
Temperature A causes disease B
NDVI threshold C means disease D
```

Such values must come from the verified disease knowledge base, validated field data, or trained models.

The engine only performs the generic temporal mathematics required to represent progression.

## Dataset rule

The included CSV rows are minimal executable placeholders.

Replace them with the actual verified records while preserving:

```text
07_disease_events/
├── disease_events.csv
├── disease_event_evidence.csv
└── progression_observations.csv
```

If the supplied dataset later contains additional Step 7 files, keep them in this directory. This package does not require renaming them.
