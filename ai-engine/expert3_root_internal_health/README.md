# STEP 10 — Expert 3: Root/Internal Health

This package adds **STEP 10 — Expert 3: Root/Internal Health** without changing
the architecture established for the previous expert stages.

## Position

```text
STEP 4 — Observation / Image / Video
        ↓
STEP 8 — Expert 1: Visual Health
        ↓
STEP 9 — Expert 2: Chemical/Pesticide Damage
        ↓
STEP 10 — Expert 3: Root/Internal Health
        ↓
Experts 4–7
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
    └── expert3_root_internal_health/
        ├── api/
        ├── schemas/
        ├── services/
        ├── preprocessing/
        ├── inference/
        ├── postprocessing/
        ├── models/
        └── storage/
```

Previous expert modules are not renamed, removed, or merged.

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
└── 10_expert3_root_internal_health/
    ├── expert3_observations.csv
    └── expert3_labels.csv
```

The Step 10 directory is additive.

## Expert 3 responsibility

Expert 3 is responsible for evidence related to **root/internal health** from
whatever observation modality is actually available to the supplied model.

The implementation boundary is:

```text
Observation
    ↓
Input validation
    ↓
Model-specific preprocessing
    ↓
Supplied trained Expert 3 model
    ↓
Prediction
    ↓
Post-processing
    ↓
Structured root/internal-health evidence
```

This module does not assume that root/internal health can be observed from an
ordinary RGB image. The actual modality must match the supplied model and
dataset.

For example, if your actual model expects a specific imaging modality, sensor
representation, cross-section image, or another input type, the adapter must
implement that documented contract rather than converting it blindly to RGB.

## Trained model

No trained model is fabricated.

A TorchScript loading adapter is included:

```text
models/expert3_root_internal_health/
├── production/
├── staging/
└── archived/
```

Place the supplied artifact in `production/`.

Test:

```bash
python scripts/test_expert3.py     models/expert3_root_internal_health/production/model.pt     path/to/input.jpg
```

The loader handles model loading and CPU/CUDA selection.

The actual `predict()` implementation remains model-specific.

## Why model-specific inference is intentionally unfinished

Without the supplied trained model and its documented input/output contract,
the following cannot be safely inferred:

```text
input modality
input dimensions
channel order
normalization
tensor layout
class names
class IDs
output tensor structure
detection/segmentation format
confidence semantics
```

The package therefore does not invent them.

## Model candidates

The correct architecture depends on the actual Expert 3 dataset and modality.

If the dataset is image classification:

```text
EfficientNet
ConvNeXt
ViT
```

If localized abnormalities are annotated:

```text
YOLO family
RT-DETR
```

If affected regions require pixel masks:

```text
U-Net
DeepLab
Mask R-CNN
```

If the data is not ordinary RGB imagery, select an architecture appropriate to
the actual modality instead of forcing an RGB computer-vision model.

These are candidates to benchmark, not a claim that one is best.

## Evaluation

Use the metrics appropriate to the actual task:

```text
Classification:
  Precision
  Recall
  F1
  Confusion matrix

Detection:
  Precision
  Recall
  mAP
  false-negative rate

Segmentation:
  IoU
  Dice
  pixel precision/recall
```

Also record:

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
basic image-quality classification
```

It does not impose:

```text
specific resolution
specific normalization
RGB/BGR convention
ImageNet mean/std
specific crop strategy
```

Those belong to the actual model adapter.

## Output

The stable evidence contract contains:

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
  "expert": "EXPERT_3_ROOT_INTERNAL_HEALTH",
  "observation_id": "OBS-001",
  "model_name": "user_provided_root_internal_health_model",
  "model_version": "provided",
  "task": "DETECTION",
  "detections": [],
  "processing_time_ms": 0.0,
  "evidence_quality": "ACCEPTABLE",
  "status": "COMPLETED"
}
```

The empty detection list is only the schema example.

## API

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:

```text
POST /api/v1/experts/expert3/root-internal-health/analyze
GET  /api/v1/experts/expert3/root-internal-health/model
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

The tests use a fake model only to verify the service contract. They do not
claim real root/internal-health detection.

Dataset structure check:

```bash
python scripts/validate_expert3_dataset.py
```

## Evidence boundary

Expert 3 returns evidence.

It does NOT independently output:

```text
final disease diagnosis
final causal explanation
treatment
pesticide recommendation
IPM recommendation
farm-wide risk
```

Those belong to the later multimodal fusion and decision stages.

## Relationship to the MoE

```text
Expert 1
Visual Health
      │
      ├──────────────┐
      │              │
Expert 2             │
Chemical/Pesticide   │
Damage               │
      │              │
      └──────┬───────┘
             ↓
        Expert 3
   Root/Internal Health
             │
             ↓
       Experts 4–7
             │
             ↓
 Structured Evidence Fusion
             │
             ↓
          Expert 8
```

Expert 3 should remain independent so the evidence-fusion layer can compare
root/internal evidence with visual, chemical/pesticide, environmental, and
other expert evidence.

## No-hallucination rule

This implementation does not claim that any specific:

```text
root symptom
internal symptom
pathogen
nutrient deficiency
chemical
pesticide
soil condition
```

can be inferred by Expert 3 unless that relationship is supported by the actual
dataset/model and verified knowledge.

The model supplied by you is the source of truth for the concrete inference
adapter.

## Not included in Step 10

```text
Expert 4
Expert 5
Expert 6
Expert 7
Expert 8
evidence fusion
final diagnosis
treatment recommendation
IPM recommendation
model training
MLflow lifecycle
Kafka integration
PostgreSQL integration
```

Those remain later architectural stages.
