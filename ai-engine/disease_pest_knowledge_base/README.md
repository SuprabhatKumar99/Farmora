# STEP 2 — Disease & Pest Knowledge Base

Implements **only Step 2** of the AI Engine roadmap.

## Dataset structure — unchanged

```text
02_disease_pest_knowledge/
├── diseases.csv
├── pests.csv
├── symptoms.csv
├── disease_progression.csv
├── disease_conditions.csv
└── management.csv
```

No file is renamed, removed, merged, or replaced.

## Implementation

```text
CSV files
   ↓
DiseasePestKnowledgeRepository
   ↓
DiseasePestKnowledgeValidator
   ↓
DiseasePestKnowledgeService
   ↓
Later experts
```

Implemented:
- CSV loading
- Disease lookup
- Pest lookup by crop
- Symptom lookup by disease
- Disease progression lookup
- Disease-condition lookup
- Management lookup
- duplicate-ID validation
- disease/symptom foreign-key validation
- crop consistency validation
- tests
- validation script

The exact columns provided for diseases.csv, pests.csv and symptoms.csv are preserved.

For disease_progression.csv, disease_conditions.csv and management.csv, the provided structure names the files but does not define their columns. The loader therefore does not invent a rigid schema for them.

The included rows are minimal executable examples only. Replace them with the actual verified dataset.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_knowledge.py
pytest -q
```

Windows activation:

```powershell
.venv\Scripts\activate
```

## Example

```python
from pathlib import Path
from app.knowledge.repository import DiseasePestKnowledgeRepository
from app.knowledge.service import DiseasePestKnowledgeService
from app.knowledge.validator import DiseasePestKnowledgeValidator

base = Path("data/crop_health_dataset/02_disease_pest_knowledge")
repo = DiseasePestKnowledgeRepository(base)
DiseasePestKnowledgeValidator().validate(repo)

service = DiseasePestKnowledgeService(repo)
context = service.get_disease_context("D001")
print(context)
```

The disease context contains:

```text
disease
symptoms
progression
conditions
management
```

## Core relationships

```text
crop
 ├── diseases
 │    ├── symptoms
 │    ├── disease_progression
 │    ├── disease_conditions
 │    └── management
 └── pests
```

The implementation preserves `crop_id` and `disease_id` as relationship keys.

## Boundary

This step does not implement:
- farm digital profile
- observations
- environment
- remote sensing
- disease-event analytics
- MoE experts
- evidence fusion
- Expert 8
- Kafka
- PostgreSQL
