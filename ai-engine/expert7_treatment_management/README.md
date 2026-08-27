# STEP 14 — Expert 7: Treatment / Management

This package adds **STEP 14 — Expert 7: Treatment / Management** while
preserving the project structure established through Steps 1–13.

## Position

```text
STEP 8  — Expert 1: Visual Health
STEP 9  — Expert 2: Chemical/Pesticide Damage
STEP 10 — Expert 3: Root/Internal Health
STEP 11 — Expert 4: Whole Crop Health
STEP 12 — Expert 5: Environment & Weather
STEP 13 — Expert 6: Prevention / IPM
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
    ├── expert6_prevention_ipm/
    └── expert7_treatment_management/
        ├── api/
        ├── schemas/
        ├── services/
        ├── preprocessing/
        ├── inference/
        ├── postprocessing/
        ├── models/
        └── storage/
```

No previous expert directory is renamed, removed, or replaced.

## Important correction from previous stages

The `inference/` module is intentionally implemented here.

```text
models/
    model implementation + loading
        ↓
inference/
    actual model execution
        ↓
postprocessing/
    structural output normalization
        ↓
services/
    application orchestration
```

This follows the common AI-engine architecture.

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
├── 13_expert6_prevention_ipm/
└── 14_expert7_treatment_management/
    ├── expert7_cases.csv
    └── expert7_treatments.csv
```

The included rows are placeholders for structure/testing only.

## Expert 7 responsibility

Expert 7 handles **Treatment / Management** evidence and/or candidate
management actions.

The intended pipeline is:

```text
Verified case/context
        ↓
Preprocessing
        ↓
Expert 7 inference
        ↓
Prediction adaptation
        ↓
Post-processing
        ↓
Structured treatment/management evidence
```

Expert 7 is not the final decision maker.

## Critical evidence boundary

Concrete treatment instructions are high-impact agricultural decisions.

This implementation therefore does NOT invent:

```text
pesticide product names
active ingredients
dosage
application rate
spray concentration
waiting period
pre-harvest interval
number of applications
tank mixing
legal restrictions
crop-specific treatment instructions
```

Concrete treatment information must come from the verified project knowledge
base and appropriate validated agricultural sources/model outputs.

## Trained model

No trained model is fabricated.

Model lifecycle:

```text
models/
└── expert7_treatment_management/
    ├── production/
    ├── staging/
    └── archived/
```

Place the supplied model in:

```text
models/expert7_treatment_management/production/
```

Test:

```bash
python scripts/test_expert7.py     models/expert7_treatment_management/production/model.pt     path/to/case.csv
```

The loader supports TorchScript and selects CUDA when available, otherwise CPU.

## Model contract

Before implementing the supplied model adapter, verify:

```text
input feature schema
feature order
feature encoding
diagnosis/context representation
candidate treatment representation
output labels
ranking semantics
confidence/score semantics
evidence representation
```

The implementation deliberately does not guess these.

## Model candidates

The correct model depends on the actual Expert 7 dataset.

### Treatment classification

If the dataset maps a case to an established treatment-management class:

```text
Logistic Regression
Random Forest
Gradient Boosting
XGBoost / LightGBM
Neural classifier
```

### Treatment ranking

If the system receives a set of allowed candidate actions and must rank them:

```text
Learning-to-Rank
Gradient-boosted ranking
Pairwise ranking
Listwise ranking
```

### Recommendation

If the dataset contains case → validated action pairs:

```text
Content-based recommendation
Hybrid recommendation
Retrieval + ranking
Neural recommendation
```

### Knowledge-driven treatment management

If the treatment is determined by verified agricultural rules, the preferred
architecture may be retrieval/rules + validation rather than allowing a model
to freely generate treatment instructions.

Conceptually:

```text
Verified Knowledge Base
        +
Experts 1–6 evidence
        ↓
Candidate treatment/management actions
        ↓
Validation
        ↓
Expert 7 evidence
        ↓
Expert 8 decision
```

These are candidate approaches only. The final model must be selected using
the actual dataset and evaluation results.

## Inference architecture

```text
Case Input
    ↓
Preprocessor
    ↓
TreatmentManagementInferenceEngine
    ↓
Supplied Model
    ↓
Raw Prediction
    ↓
TreatmentPredictionAdapter
    ↓
TreatmentManagementPostprocessor
    ↓
TreatmentManagementResult
```

### `inference/inference_engine.py`

Owns the actual call to the loaded model.

### `inference/prediction_adapter.py`

Converts model-specific output into:

```text
treatment_id
treatment_type
priority
evidence_ids
validation_required
```

### `postprocessing/postprocessor.py`

Performs structural processing such as priority ordering.

It does not introduce agricultural treatment rules.

## Output

```json
{
  "expert": "EXPERT_7_TREATMENT_MANAGEMENT",
  "case_id": "CASE-001",
  "model_name": "user_provided_treatment_management_model",
  "model_version": "provided",
  "task": "RECOMMENDATION",
  "treatments": [],
  "processing_time_ms": 0.0,
  "evidence_quality": "ACCEPTABLE",
  "status": "COMPLETED"
}
```

The empty treatment list is only a schema example.

Each treatment candidate contains:

```text
treatment_id
treatment_type
priority
evidence_ids
validation_required
```

## Validation flag

Every candidate has:

```text
validation_required
```

The default is `true`.

This is intentional. The Expert 7 output should not automatically be treated
as an approved treatment instruction.

## API

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:

```text
POST /api/v1/experts/expert7/treatment-management/analyze
GET  /api/v1/experts/expert7/treatment-management/model
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

The tests use a fake model only to validate the software contract. They do not
represent real treatment recommendations.

Dataset validation:

```bash
python scripts/validate_expert7_dataset.py
```

## Evaluation

Metrics depend on the actual task.

For classification:

```text
Precision
Recall
F1
Confusion matrix
Per-class recall
False-negative rate
```

For ranking/recommendation:

```text
Precision@K
Recall@K
MAP@K
NDCG@K
```

Also evaluate:

```text
unsupported-action rate
invalid-action rate
coverage
evidence traceability
```

For safety-critical agricultural outputs, evaluation must include whether the
system can abstain or request validation when evidence is insufficient.

## Evidence traceability

Every treatment candidate should be traceable:

```text
Treatment candidate
        ↓
Evidence IDs
        ↓
Observed farm/crop context
        +
Verified knowledge
        +
Expert evidence
```

This allows the later evidence-fusion layer and Expert 8 to inspect the basis
of the candidate.

## Relationship with Expert 6

Expert 6 focuses on:

```text
Prevention / IPM
```

Expert 7 focuses on:

```text
Treatment / Management
```

They should remain separate:

```text
Expert 6
Prevention / IPM
       │
       ├──────────────┐
       │              │
       ▼              ▼
Knowledge        Expert 7
                 Treatment /
                 Management
                      │
                      ▼
              Evidence Fusion
```

Expert 7 should not silently duplicate Expert 6.

## Relationship with Expert 8

```text
Experts 1–7
     ↓
Structured Evidence Fusion
     ↓
Expert 8 — Agricultural Decision LLM
     ↓
Final Crop Health Decision
```

Expert 7 supplies treatment/management evidence; Expert 8 resolves the
overall context and generates the final decision according to the system's
validated rules.

## No-hallucination rule

This step does not invent concrete treatment instructions.

The following must originate from verified data/knowledge/model contracts:

```text
treatment identity
active ingredient
dose
rate
application method
timing
frequency
restrictions
crop-specific instructions
```

If required evidence is unavailable, the system should preserve that
uncertainty rather than fabricate a treatment.

## Not included in Step 14

```text
Structured Evidence Fusion
Expert 8
Final crop-health decision
Final farmer advisory
Kafka integration
PostgreSQL integration
MLflow lifecycle
```

Those remain later stages of the architecture.
