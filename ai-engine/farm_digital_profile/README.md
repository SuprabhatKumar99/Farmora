# STEP 3 — Farm Digital Profile

This package implements **only Step 3** of the AI Engine roadmap.

The project and dataset structure is preserved exactly:

```text
crop_health_dataset/
└── 03_farm/
    ├── farms.csv
    ├── fields.csv
    ├── zones.csv
    └── crop_cycles.csv
```

The Farm Digital Profile connects:

```text
Farm → Zone → Crop Cycle → Crop / Variety / Growth Stage
```

## Implemented

- CSV repository/loader
- Farm lookup
- Field loading
- Zone lookup
- Crop-cycle lookup
- Farm digital profile service
- Zone profile service
- Duplicate ID validation
- Farm/zone/crop-cycle relationship validation
- Farm/zone consistency validation
- Tests
- Validation script

## Important: structure is not modified

No dataset file is renamed, merged, removed, or moved.

The exact schemas explicitly provided for:

```text
farms.csv
zones.csv
crop_cycles.csv
```

are preserved.

The supplied dataset document identifies `fields.csv` as part of `03_farm/` but does not define its columns. Therefore this implementation loads `fields.csv` without imposing an invented schema.

The included CSV rows are minimal executable examples only. Replace them with your real verified dataset.

## Architecture

```text
03_farm/*.csv
      ↓
FarmDigitalProfileRepository
      ↓
FarmDigitalProfileValidator
      ↓
FarmDigitalProfileService
      ↓
Farm context for later AI stages
```

Later experts should consume the profile through the service rather than reading CSV files directly.

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

## Validate

```bash
python scripts/validate_farm.py
```

Expected:

```text
Farm Digital Profile validation: PASS
```

## Test

```bash
pytest -q
```

## Example

```python
from pathlib import Path

from app.knowledge.repository import FarmDigitalProfileRepository
from app.knowledge.service import FarmDigitalProfileService
from app.knowledge.validator import FarmDigitalProfileValidator

base = Path("data/crop_health_dataset/03_farm")

repository = FarmDigitalProfileRepository(base)
FarmDigitalProfileValidator().validate(repository)

service = FarmDigitalProfileService(repository)

profile = service.get_farm_profile("F001")

print(profile.model_dump())
```

## Profile output

The profile contains:

```text
farm
fields
zones
crop_cycles
```

A zone profile contains:

```text
zone
crop_cycles
```

## Relationship validation

The implementation verifies:

```text
zones.farm_id
      ↓
farms.farm_id
```

and:

```text
crop_cycles.farm_id
      ↓
farms.farm_id
```

and:

```text
crop_cycles.zone_id
      ↓
zones.zone_id
```

It also verifies that the `farm_id` stored in a crop cycle agrees with the `farm_id` of the referenced zone.

## Boundary

This step does not implement:

- observations
- image/video processing
- environment/sensors
- remote sensing
- disease events
- Experts 1–8
- evidence fusion
- decision engine
- Kafka
- PostgreSQL

Those are later roadmap steps.
