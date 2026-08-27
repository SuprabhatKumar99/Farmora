# STEP 18 — Validation & Ground Truth

This package adds **STEP 18 — Validation & Ground Truth** without changing
or removing the established Expert 1–7, Structured Evidence Fusion, Expert 8,
or Decision/Risk/Recommendation output structure.

## Architecture position

```text
Experts 1–7
     ↓
Structured Evidence Fusion
     ↓
Expert 8 — Core Agricultural Decision AI
     ↓
Decision / Risk / Recommendation Outputs
     ↓
┌──────────────────────────────────────────┐
│ STEP 18 — VALIDATION & GROUND TRUTH     │
│                                          │
│ Ground-truth management                 │
│ Verification status                     │
│ Prediction comparison                   │
│ Evaluation metrics                      │
│ Mismatch reporting                      │
│ Traceability                            │
└──────────────────────┬───────────────────┘
                       ↓
                 Model Evaluation
                 / Improvement
```

## Project structure

```text
app/
├── experts/
│   ├── expert1_visual_health/
│   ├── expert2_chemical_pesticide_damage/
│   ├── expert3_root_internal_health/
│   ├── expert4_whole_crop_health/
│   ├── expert5_environment_weather/
│   ├── expert6_prevention_ipm/
│   └── expert7_treatment_management/
│
├── evidence_fusion/
├── expert8_core_ai/
├── decision_outputs/
│
└── validation_ground_truth/
    ├── api/
    ├── schemas/
    ├── services/
    ├── validation/
    ├── ground_truth/
    ├── metrics/
    ├── datasets/
    ├── traceability/
    └── storage/
```

No previous structure is renamed or removed.

# 1. Purpose

Step 18 establishes a controlled boundary between:

```text
Model prediction
```

and:

```text
Verified reference / ground truth
```

The goal is to measure model behavior against reviewed reference data rather
than assuming model outputs are correct.

# 2. Ground-truth lifecycle

```text
Candidate Case
     ↓
Annotation
     ↓
Review
     ↓
Verification
     ↓
Ground Truth
     ↓
Validation Dataset
     ↓
Model Evaluation
```

The implementation defines:

```text
DRAFT
REVIEWED
VERIFIED
REJECTED
```

Only `VERIFIED` records are usable by the validation service as ground truth.

# 3. Ground truth record

Each record contains:

```text
case_id
target_type
ground_truth
status
split
annotator_ids
reviewer_ids
source_ids
notes
```

This supports traceability without claiming that a label is correct merely
because it exists.

# 4. Verification rule

A record marked:

```text
VERIFIED
```

must have either:

```text
reviewer_ids
```

or:

```text
source_ids
```

This is a metadata integrity check.

It is not a substitute for qualified agricultural review.

# 5. Ground-truth principle

Ground truth must come from verified project sources.

Examples may include, depending on the actual project protocol:

```text
qualified expert annotation
laboratory-confirmed case
verified field observation
validated historical case
verified agronomic record
```

The implementation does not assume which of these is available.

Do not convert an unverified prediction into ground truth.

# 6. Dataset splits

The schema supports:

```text
TRAIN
VALIDATION
TEST
```

The actual split policy must be defined by the project.

Important:

Do not randomly split correlated observations in a way that leaks the same
farm, field, plant, image sequence, or case across train and test sets.

The correct grouping key depends on the dataset and should be defined during
dataset curation.

# 7. Validation flow

```text
Expert 8 / Model Prediction
             ↓
       Validation Request
             ↓
       Ground Truth Check
             ↓
       Compatibility Check
             ↓
       Metric Evaluation
             ↓
       Mismatch Report
             ↓
       Traceability Report
```

# 8. Current metric implementation

For declared classification targets, Step 18 calculates:

```text
Accuracy
Macro Precision
Macro Recall
Macro F1
```

For N samples:

```text
Accuracy = correct predictions / N
```

Macro precision is:

```text
Precision_macro = (1/K) Σ Precision_k
```

Macro recall is:

```text
Recall_macro = (1/K) Σ Recall_k
```

Macro F1 is:

```text
F1_macro = (1/K) Σ F1_k
```

where K is the number of classes represented by the evaluator.

These formulas are standard classification metrics.

# 9. Metric boundary

The current implementation evaluates only an explicit classification contract:

```json
Ground truth:
{
  "label": "A"
}

Prediction:
{
  "label": "A"
}
```

It does not pretend that:

```text
diagnosis
severity
risk
treatment
```

are classification targets unless the project explicitly defines them that way.

For regression, detection, segmentation, ranking, calibration, or structured
generation, dedicated evaluators should be added later rather than reusing
classification metrics incorrectly.

# 10. Mismatch handling

If:

```text
ground_truth.label != prediction.label
```

the result contains a mismatch record.

Example:

```json
{
  "field": "label",
  "ground_truth": "A",
  "prediction": "B"
}
```

The system does not automatically change the prediction or ground truth.

# 11. Traceability

Each validation result records:

```text
case_id
ground_truth_source_ids
annotator_ids
reviewer_ids
ground_truth_status
prediction_evidence_ids
prediction_model_name
prediction_model_version
```

This connects evaluation back to both:

```text
reference data
```

and:

```text
model output
```

# 12. No-hallucination rule

Step 18 must never invent:

```text
ground-truth labels
laboratory results
expert annotations
disease confirmations
model accuracy
model performance
```

If a verified target is unavailable:

```text
GROUND_TRUTH_NOT_USABLE
```

or:

```text
NO_COMPATIBLE_CLASSIFICATION_TARGET
```

is returned.

# 13. Important distinction

Ground truth is not:

```text
Expert 8 prediction
```

and it is not:

```text
Step 17 recommendation
```

The relationship is:

```text
Verified reference
       ↓
Ground Truth

Model
       ↓
Prediction

Ground Truth + Prediction
       ↓
Validation
```

# 14. API

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoint:

```text
POST /api/v1/validation-ground-truth/validate
```

Health:

```text
GET /api/v1/validation-ground-truth/health
GET /health
GET /ready
```

Example:

```json
{
  "case_id": "CASE-001",
  "prediction": {
    "label": "CLASS_A",
    "reasoning_evidence_ids": ["E1"],
    "model_name": "expert8-model",
    "model_version": "1.0"
  },
  "ground_truth": {
    "case_id": "CASE-001",
    "target_type": "classification",
    "ground_truth": {
      "label": "CLASS_A"
    },
    "status": "VERIFIED",
    "reviewer_ids": ["reviewer-1"],
    "source_ids": ["source-1"]
  }
}
```

The example values are structural examples, not real agricultural ground
truth.

# 15. Testing

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
pytest -q
```

Validate dataset structure:

```bash
python scripts/validate_step18_dataset.py
```

# 16. Dataset structure

```text
data/crop_health_dataset/
└── 18_validation_ground_truth/
    ├── ground_truth_cases.csv
    ├── validation_cases.csv
    └── README.md
```

The included CSV rows are structural examples only.

They must not be treated as actual agricultural ground truth.

# 17. Recommended real validation dataset design

The actual project dataset should preserve:

```text
case_id
farm_id / field_id where appropriate
observation_id
source IDs
crop
variety
growth stage
timestamp
location/zone
reference label
reference confidence if defined by protocol
annotator
reviewer
verification status
split
```

Only include fields that are actually available and defined by the project.

# 18. Expert validation

Experts 1–7 should be evaluated against expert-specific ground truth.

Conceptually:

```text
Expert 1 prediction
      ↕
Visual Health Ground Truth

Expert 2 prediction
      ↕
Chemical/Pesticide Damage Ground Truth

Expert 3 prediction
      ↕
Root/Internal Health Ground Truth

...
```

The exact metric must match the task.

For example:

```text
classification → classification metrics
object detection → detection metrics
segmentation → segmentation metrics
regression → regression metrics
```

Do not use a metric that does not match the model task.

# 19. Expert 8 validation

Expert 8 should be evaluated on:

```text
Evidence grounding
Decision correctness
Diagnosis correctness
Risk correctness
Severity correctness
Conflict handling
Missing-evidence handling
Abstention / validation behavior
Structured-output validity
```

The exact scoring protocol should be defined from the actual target schema and
verified dataset.

# 20. Recommendation validation

Treatment/management recommendations require special handling.

Evaluation should verify against the project's authoritative reference
sources.

Do not treat a language-model recommendation as ground truth merely because
it sounds plausible.

Where a recommendation requires professional, laboratory, regulatory, or
label-based validation, that validation must come from the appropriate source.

# 21. Data leakage prevention

A major validation requirement is preventing leakage.

Potentially correlated samples include:

```text
same plant
same farm
same field
same disease event
adjacent video frames
near-duplicate images
same observation session
```

These should not be allowed to create artificially optimistic test results.

The exact grouping strategy depends on the actual dataset.

# 22. Evaluation reproducibility

Each evaluation should record:

```text
dataset version
ground-truth version
model name
model version
evaluation date
split
metric configuration
code version
```

The current implementation exposes model and ground-truth traceability fields;
the complete experiment/versioning system can be integrated with the existing
ML lifecycle later.

# 23. Statistical interpretation

A single metric should not be treated as proof of production reliability.

For example:

```text
Accuracy = 95%
```

does not by itself establish:

```text
safe agricultural deployment
```

Evaluation should also consider:

```text
class imbalance
per-class performance
false negatives
false positives
confidence calibration
domain shift
farm-level generalization
geographic generalization
seasonal generalization
```

These require actual evaluation data; Step 18 does not invent such results.

# 24. Validation feedback loop

```text
Model Prediction
      ↓
Ground Truth Comparison
      ↓
Error Analysis
      ↓
Failure Cases
      ↓
Dataset Improvement
      ↓
Retraining / Fine-tuning
      ↓
New Model Version
      ↓
Re-validation
```

This supports the larger project feedback loop.

# 25. Relationship with MLflow

The existing MLflow lifecycle can later record:

```text
dataset version
ground-truth version
model version
accuracy
precision
recall
F1
evaluation configuration
```

Step 18 does not require MLflow to execute its local validation logic.

# 26. Production boundary

Step 18 is primarily an evaluation/quality layer.

It should not directly modify:

```text
production predictions
ground truth
model weights
```

A model should be promoted only after passing the project's defined
evaluation and review process.

# 27. Final architecture

```text
                   Experts 1–7
                        ↓
              Evidence Fusion
                        ↓
                   Expert 8
                        ↓
          Decision/Risk/Recommendation
                        ↓
               Production Output
                        │
                        │
                        ▼
              ┌─────────────────┐
              │ STEP 18         │
              │ Validation      │
              │ & Ground Truth  │
              └───────┬─────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Ground Truth  Metrics   Traceability
          │           │           │
          └───────────┼───────────┘
                      ▼
                 Error Analysis
                      ↓
              Model Improvement
```

# 28. Not included

```text
New expert model
Model training
Automatic relabeling
Automatic model promotion
Automatic production deployment
Fabricated ground truth
Laboratory verification
Regulatory certification
```

Those require actual project data, procedures, or external systems.

# 29. Final principle

The validation chain must remain:

```text
Verified Ground Truth
        +
Actual Model Prediction
        ↓
Objective Evaluation
        ↓
Traceable Result
        ↓
Error Analysis
        ↓
Model / Dataset Improvement
```

Never reverse the relationship:

```text
Model prediction → ground truth
```

A model output can be evaluated against ground truth, but it cannot become
ground truth merely because the model produced it.
