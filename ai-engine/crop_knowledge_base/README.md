# STEP 1 — Crop Knowledge Base

Implements only Step 1 of the SIH 2026 AI Engine roadmap, following the supplied dataset structure:

01_crop_knowledge/
- crops.csv
- varieties.csv
- growth_stages.csv
- crop_lifecycle.csv
- crop_requirements.csv

## Included
- CSV repository using pandas
- Pydantic models
- schema validation
- duplicate ID validation
- foreign-key validation
- growth-stage range validation
- crop/variety context service
- tests
- validation script

The included CSVs are minimal executable examples matching the supplied structure. Replace them with your actual verified dataset before real agricultural use.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_knowledge.py
pytest -q
```

Windows:
```powershell
.venv\Scripts\activate
```

## Service example

```python
from pathlib import Path
from app.knowledge.repository import CropKnowledgeRepository
from app.knowledge.service import CropKnowledgeService
from app.knowledge.validator import CropKnowledgeValidator

base = Path("data/crop_health_dataset/01_crop_knowledge")
repo = CropKnowledgeRepository(base)
CropKnowledgeValidator().validate(repo)

service = CropKnowledgeService(repo)
context = service.get_crop_context("C001", "V001")
print(context.model_dump())
```

Returned context:
- crop
- varieties
- growth_stages
- crop_lifecycle
- requirements

Experts must use the knowledge service rather than reading CSV files directly.

This step does not implement disease/pest knowledge, farm profiles, observations, Experts 1–8, Kafka, PostgreSQL, or decision logic.
