# STEP 13 — Expert 6: Prevention / IPM

This package adds **STEP 13 — Expert 6: Prevention / IPM** while preserving
the structure established through Steps 1–12.

## Position

```text
STEP 8  — Expert 1: Visual Health
STEP 9  — Expert 2: Chemical/Pesticide Damage
STEP 10 — Expert 3: Root/Internal Health
STEP 11 — Expert 4: Whole Crop Health
STEP 12 — Expert 5: Environment & Weather
STEP 13 — Expert 6: Prevention / IPM
             ↓
STEP 14 — Expert 7: Treatment / Management
             ↓
Structured Evidence Fusion
             ↓
Expert 8 — Agricultural Decision LLM
```

## Project structure

```text
app/
└── experts/
    ├── expert1_visual_health/
    ├── expert2_chemical_pesticide_damage/
    ├── expert3_root_internal_health/
    ├── expert4_whole_crop_health/
    ├── expert5_environment_weather/
    └── expert6_prevention_ipm/
        ├── api/
        ├── schemas/
        ├── services/
        ├── preprocessing/
        ├── inference/
        ├── postprocessing/
        ├── models/
        └── storage/
```

The previous expert structures are not renamed or replaced.

## Dataset structure

```text
crop_health_dataset/
├── 01_crop_knowledge/
├── 02_disease_pest_knowledge/
├── 03_farm/
├── 04_observations/
├── 05_environment/
├── 06_remote_sensing/
├── 07_disease_events/
├── 08_expert1_visual_health/
├── 09_expert2_chemical_pesticide_damage/
├── 10_expert3_root_internal_health/
├── 11_expert4_whole_crop_health/
├── 12_expert5_environment_weather/
└── 13_expert6_prevention_ipm/
    ├── expert6_cases.csv
    └── expert6_actions.csv
```

The example rows are placeholders for structure/testing only. They are not
agricultural recommendations.

## Expert 6 responsibility

Expert 6 handles **prevention and Integrated Pest Management (IPM)** evidence
and/or action candidates.

The intended boundary is:

```text
Verified case/context
        ↓
Input validation
        ↓
Knowledge/model-specific processing
        ↓
Expert 6 model / rule component
        ↓
Candidate prevention/IPM actions
        ↓
Structured Expert 6 evidence
```

The final agricultural decision remains downstream.

## Critical safety and evidence boundary

This step does not fabricate:

```text
pesticide products
active ingredients
application rates
dosages
spray intervals
legal restrictions
crop-specific treatment rules
disease thresholds
pest thresholds
```

Those details must come from the verified Crop Knowledge Base, Disease & Pest
Knowledge Base, approved agricultural sources, and/or the supplied model/data.

The Expert 6 model should not be treated as a substitute for those sources.

## Trained model

No trained model is fabricated.

Model lifecycle:

```text
models/
└── expert6_prevention_ipm/
    ├── production/
    ├── staging/
    └── archived/
```

Place your supplied model in `production/`.

Test:

```bash
python scripts/test_expert6.py     models/expert6_prevention_ipm/production/model.pt     path/to/case.csv
```

The loader supports TorchScript and automatically selects CUDA when available,
otherwise CPU.

## Model contract

Before implementing the concrete adapter, verify:

```text
input features
feature order
feature encoding
knowledge-base identifiers
missing-value handling
action labels
output structure
ranking/score semantics
confidence semantics
```

The adapter does not guess these.

## Suitable model approaches

The correct approach depends on the actual Expert 6 dataset.

### Classification

If the model predicts an established prevention/IPM category:

```text
Logistic Regression
Random Forest
Gradient Boosting
XGBoost / LightGBM
Neural network
```

### Ranking

If the task ranks multiple candidate prevention actions:

```text
Learning-to-Rank models
Gradient-boosted ranking
Pairwise ranking
Listwise ranking
```

### Recommendation

If the dataset contains case → action examples:

```text
Content-based recommendation
Hybrid recommendation
Neural recommendation
Retrieval + ranking
```

### Knowledge/rule-driven IPM

If the actual requirement is primarily deterministic agricultural guidance,
a verified knowledge/rule layer may be more appropriate than training a model
to invent recommendations.

For this project, the safest architecture is:

```text
Verified Knowledge Base
        +
Model-derived evidence
        ↓
Candidate Prevention/IPM Actions
        ↓
Evidence Fusion / Expert 8
```

The final model choice must be made from the actual dataset and validation
results.

## Input processing

The generic preprocessing supports:

```text
CSV
Parquet
JSON
```

It performs only:

```text
path validation
format validation
data loading
empty-input validation
```

It does not invent:

```text
feature engineering
disease thresholds
pest thresholds
risk scores
action rules
```

Those must match the real model/knowledge contract.

## Output contract

Expert 6 returns:

```text
expert
case_id
model_name
model_version
task
actions
processing_time_ms
evidence_quality
status
error_code
error_message
```

Each action contains:

```text
action_id
action_type
priority
evidence_ids
```

Example:

```json
{
  "expert": "EXPERT_6_PREVENTION_IPM",
  "case_id": "CASE-001",
  "model_name": "user_provided_prevention_ipm_model",
  "model_version": "provided",
  "task": "RECOMMENDATION",
  "actions": [],
  "processing_time_ms": 0.0,
  "evidence_quality": "ACCEPTABLE",
  "status": "COMPLETED"
}
```

The empty action list is only a schema example.

## API

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:

```text
POST /api/v1/experts/expert6/prevention-ipm/analyze
GET  /api/v1/experts/expert6/prevention-ipm/model
GET  /health
GET  /ready
```

Example:

```json
{
  "case_id": "CASE-001",
  "input_path": "path/to/case.csv",
  "model_version": "production"
}
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Tests

```bash
pytest -q
```

The tests use a fake model only to verify the software interface. They do not
represent real IPM recommendations.

Dataset validation:

```bash
python scripts/validate_expert6_dataset.py
```

## Evaluation

The metrics depend on the actual task.

For classification:

```text
Precision
Recall
F1
Confusion matrix
Per-class recall
```

For ranking/recommendation:

```text
Precision@K
Recall@K
MAP@K
NDCG@K
```

For any learned recommendation system, also evaluate:

```text
coverage
invalid-action rate
unsupported-action rate
```

Most importantly, evaluate whether every generated action can be traced to
valid evidence and an approved knowledge source.

## Explainability / evidence trace

Every action should ultimately be traceable to evidence.

Conceptually:

```text
Action
  ↓
Evidence IDs
  ↓
Observed context / verified knowledge
  ↓
Supporting source
```

This becomes important when Expert 8 resolves conflicts between Expert 6 and
the other experts.

## Relationship with Knowledge Base

Expert 6 should not duplicate the entire agricultural knowledge base.

Instead:

```text
Crop Knowledge Base
        │
Disease & Pest Knowledge Base
        │
Farm Digital Profile
        │
Environment / Weather
        │
Experts 1–5
        │
        └─────────────┐
                      ↓
             Expert 6 Prevention/IPM
                      ↓
              Candidate actions
                      ↓
             Structured Evidence
```

## Evidence boundary

Expert 6 produces prevention/IPM evidence or candidate actions.

It does not independently decide:

```text
final diagnosis
final disease cause
final pesticide
final dosage
final treatment
final farmer advisory
```

Those remain subject to the verified knowledge base, evidence fusion, and
Expert 8 decision layer.

## No-hallucination rule

No specific prevention action, IPM rule, pesticide, biological control,
cultural practice, threshold, or application instruction is invented here.

Only verified project knowledge and the actual supplied model/data should
determine concrete recommendations.

## Not included in Step 13

```text
Expert 7
Expert 8
Structured Evidence Fusion
Final crop-health decision
Final treatment recommendation
Kafka integration
PostgreSQL integration
MLflow lifecycle
```

Those remain later stages of the architecture.
