# STEP 11 — Expert 4: Whole Crop Health

This package adds **STEP 11 — Expert 4: Whole Crop Health** while preserving the
project structure established through the previous expert stages.

## Position in the MoE

```text
STEP 8  — Expert 1: Visual Health
             ↓
STEP 9  — Expert 2: Chemical/Pesticide Damage
             ↓
STEP 10 — Expert 3: Root/Internal Health
             ↓
STEP 11 — Expert 4: Whole Crop Health
             ↓
Experts 5–7
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
    └── expert4_whole_crop_health/
        ├── api/
        ├── schemas/
        ├── services/
        ├── preprocessing/
        ├── inference/
        ├── postprocessing/
        ├── models/
        └── storage/
```

Step 11 is additive. Previous expert names are not changed.

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
└── 11_expert4_whole_crop_health/
    ├── expert4_observations.csv
    └── expert4_labels.csv
```

## Expert 4 responsibility

Expert 4 is the **whole-crop-health** expert. It produces model-derived evidence
about the crop's overall observed health state according to the labels and
task represented by the actual supplied model.

The implementation boundary is:

```text
Observation
    ↓
Validation
    ↓
Model-specific preprocessing
    ↓
Supplied Expert 4 model
    ↓
Prediction
    ↓
Post-processing
    ↓
Structured whole-crop-health evidence
```

It is deliberately not connected directly to the final decision layer.

## Important model boundary

The project description says Expert 4 covers whole-crop health, including overall
condition. That description alone does not define a specific dataset label set
or model architecture.

Therefore this implementation does NOT invent:

```text
healthy
moderate
severe
stressed
diseased
```

as actual model classes.

The real classes must come from your Expert 4 dataset/model.

## Trained model supplied by you

No trained model is fabricated.

A TorchScript loader is provided:

```text
models/expert4_whole_crop_health/
├── production/
├── staging/
└── archived/
```

Place your supplied artifact in:

```text
models/expert4_whole_crop_health/production/
```

Test loading/inference:

```bash
python scripts/test_expert4.py     models/expert4_whole_crop_health/production/model.pt     path/to/input.jpg
```

The loader selects CUDA when available and otherwise CPU.

## Model contract

The exact model contract must define:

```text
input modality
input dimensions
channel order
normalization
tensor layout
class IDs
class names
output tensor structure
confidence semantics
detection/segmentation decoding, if applicable
```

These are not guessed.

The `predict()` adapter is intentionally model-specific so an incompatible
checkpoint cannot silently produce invalid evidence.

## Model candidates

The correct model depends on the actual Expert 4 dataset.

### Whole-image classification

If each observation has one whole-crop-health label:

```text
EfficientNet
ConvNeXt
ViT
```

### Localized whole-crop abnormalities

If the dataset contains bounding-box annotations:

```text
YOLO family
RT-DETR
```

### Area/region-level health maps

If the dataset contains pixel masks:

```text
U-Net
DeepLab
Mask R-CNN
YOLO segmentation variants
```

### Multi-source / temporal inputs

If the supplied Expert 4 dataset combines multiple observations, time points,
or modalities, use an architecture designed for that actual input structure.
Do not force the data into a single-image classifier without validation.

These are candidate architectures only. The best model must be established by
evaluation on your actual dataset.

## Evaluation

For classification:

```text
Precision
Recall
F1
Confusion matrix
Per-class recall
False-negative rate
```

For detection:

```text
Precision
Recall
mAP
Per-class recall
False-negative rate
```

For segmentation:

```text
IoU
Dice
Pixel precision/recall
```

Also measure:

```text
Inference latency
GPU memory
Input-resolution sensitivity
```

## Preprocessing

The generic preprocessing performs only:

```text
path validation
extension validation
image decoding
empty-image validation
basic quality classification
```

It does not assume:

```text
specific input size
ImageNet normalization
RGB/BGR convention
specific crop/tiling strategy
```

Those must match the supplied model's training and inference contract.

## Output

The stable Expert 4 result contains:

```text
expert
observation_id
model_name
model_version
task
detections
processing_time_ms
evidence_quality
status
error_code
error_message
```

Example:

```json
{
  "expert": "EXPERT_4_WHOLE_CROP_HEALTH",
  "observation_id": "OBS-001",
  "model_name": "user_provided_whole_crop_health_model",
  "model_version": "provided",
  "task": "CLASSIFICATION",
  "detections": [],
  "processing_time_ms": 0.0,
  "evidence_quality": "ACCEPTABLE",
  "status": "COMPLETED"
}
```

The empty detection list is only a schema example.

## API

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:

```text
POST /api/v1/experts/expert4/whole-crop-health/analyze
GET  /api/v1/experts/expert4/whole-crop-health/model
GET  /health
GET  /ready
```

Example request:

```json
{
  "observation_id": "OBS-001",
  "image_path": "path/to/input.jpg",
  "model_version": "production",
  "confidence_threshold": 0.25
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

The tests use a fake model only to verify the software contract. They do not
claim real whole-crop-health detection.

Dataset structure validation:

```bash
python scripts/validate_expert4_dataset.py
```

## Evidence boundary

Expert 4 provides whole-crop-health evidence.

It does not independently provide:

```text
final diagnosis
root cause
chemical/pesticide recommendation
treatment
IPM recommendation
farm-wide risk score
final farmer advisory
```

Those belong to later evidence fusion and Expert 8.

## Relationship to Experts 1–3

```text
Expert 1 — Visual Health
        │
Expert 2 — Chemical/Pesticide Damage
        │
Expert 3 — Root/Internal Health
        │
Expert 4 — Whole Crop Health
        │
        └──────────────┐
                       ↓
              Structured Evidence
                       ↓
                  Evidence Fusion
                       ↓
                    Expert 8
```

Keeping Expert 4 independent allows the fusion layer to compare whole-crop
health evidence against specialized expert evidence.

## No-hallucination rule

This implementation does not claim that a specific visual pattern, disease,
nutrient condition, chemical, environmental condition, or treatment is proven
by Expert 4.

Only the verified dataset labels, supplied model, and later validated knowledge
should determine agricultural interpretation.

## Not included in Step 11

```text
Expert 5
Expert 6
Expert 7
Expert 8
Structured Evidence Fusion
Final diagnosis
Treatment recommendation
IPM recommendation
Farm-wide risk scoring
Model training
MLflow lifecycle
Kafka integration
PostgreSQL integration
```

Those remain later stages of the architecture.
