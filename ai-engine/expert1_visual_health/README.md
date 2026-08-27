# STEP 8 — Expert 1: Visual Health

This package implements **only STEP 8 — Expert 1: Visual Health**.

It preserves the project structure from Steps 1–7 and adds the Expert 1 module.

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
└── 08_expert1_visual_health/
    ├── expert1_observations.csv
    └── expert1_labels.csv
```

No previous dataset directory is renamed, removed, merged, or replaced.

## Application structure

```text
app/
└── experts/
    └── expert1_visual_health/
        ├── api/
        ├── schemas/
        ├── services/
        ├── preprocessing/
        ├── inference/
        ├── postprocessing/
        ├── models/
        └── storage/
```

Model lifecycle:

```text
models/
└── expert1_visual_health/
    ├── production/
    ├── staging/
    └── archived/
```

## Expert 1 responsibility

```text
Image
  ↓
Validation / decode
  ↓
Model-specific preprocessing
  ↓
User-provided trained visual model
  ↓
Prediction
  ↓
Post-processing
  ↓
Structured visual evidence
```

Expert 1 produces visual evidence. It does not produce the final agricultural decision.

It does NOT implement:

- final disease diagnosis
- treatment recommendation
- IPM recommendation
- farm-wide risk
- evidence fusion
- Expert 8 decision generation

## Trained model supplied by you

No trained model is fabricated in this package.

A TorchScript adapter is included for testing when your supplied model is in TorchScript format.

The adapter loads:

```text
model artifact
    ↓
TorchScript
    ↓
CPU or CUDA
    ↓
eval mode
```

However, the exact model input/output contract is unknown until the actual model is supplied.

Therefore `predict()` deliberately does not invent:

```text
input resolution
RGB/BGR convention
normalization mean/std
output tensor layout
class mapping
NMS behavior
segmentation mask format
```

Those must match the supplied model.

## Test without the trained model

The unit tests use a fake model only to verify the Expert 1 service architecture.

Run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

The fake prediction is:

```text
class: visual_anomaly
confidence: 0.92
bbox: [2, 3, 20, 21]
```

This is test data and is NOT a real disease prediction.

## Test your supplied TorchScript model

Place it under:

```text
models/expert1_visual_health/production/
```

Then:

```bash
python scripts/test_expert1.py     models/expert1_visual_health/production/model.pt     path/to/image.jpg
```

Before real inference, implement the model-specific tensor preprocessing and output decoder in the adapter according to the supplied model documentation.

Do not guess these details.

## Model task

The interface supports:

```text
CLASSIFICATION
DETECTION
SEGMENTATION
```

Use the task matching the actual trained model.

### Classification

Appropriate when the model predicts an image-level class.

### Detection

Appropriate when the model identifies localized visual targets and bounding boxes.

### Segmentation

Appropriate when the model predicts affected pixels/masks and affected-area measurement is required.

## Model selection

No single model is declared the best without the actual dataset, labels, class distribution, resolution, and deployment constraints.

Candidates to benchmark include:

Detection:
```text
YOLO family
RT-DETR
```

Classification:
```text
EfficientNet
ConvNeXt
ViT/DeiT family
```

Segmentation:
```text
U-Net
DeepLab
Mask R-CNN
YOLO segmentation variants
```

Select based on measured performance, not model reputation.

Evaluate:

```text
Precision
Recall
F1
mAP for detection
IoU/Dice for segmentation
False-negative rate
Inference latency
GPU memory
```

## Preprocessing

The generic layer only performs:

```text
path validation
extension validation
image decoding
empty-image validation
basic quality classification
```

Model-specific preprocessing belongs in the concrete model adapter because it must match training.

The implementation does NOT assume:

```text
640×640
ImageNet normalization
specific RGB/BGR conversion
specific crop strategy
```

## Confidence threshold

The API accepts:

```text
confidence_threshold
```

with a testing default of:

```text
0.25
```

This is not an agricultural threshold.

The correct threshold must be tuned using the actual validation dataset.

## Output

```json
{
  "expert": "EXPERT_1_VISUAL_HEALTH",
  "observation_id": "OBS-001",
  "model_name": "user_provided_visual_health_model",
  "model_version": "provided",
  "task": "DETECTION",
  "detections": [],
  "processing_time_ms": 0.0,
  "evidence_quality": "ACCEPTABLE",
  "status": "COMPLETED"
}
```

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

Model:

```text
GET /api/v1/experts/expert1/visual-health/model
```

Analysis:

```text
POST /api/v1/experts/expert1/visual-health/analyze
```

Example:

```json
{
  "observation_id": "OBS-001",
  "image_path": "data/samples/images/sample.jpg",
  "model_version": "production",
  "confidence_threshold": 0.25
}
```

## Dataset validation

```bash
python scripts/validate_expert1_dataset.py
```

## Architecture boundary

```text
STEP 4
Observation / Image / Video
        ↓
        image_path / observation_id
        ↓
STEP 8 — Expert 1
        ↓
visual evidence
        ↓
STEP 9+ Experts
        ↓
Structured Evidence Fusion
        ↓
Expert 8
```

Expert 1 should return evidence, not the final decision.

## Model versioning

Every result records:

```text
model_name
model_version
```

Recommended lifecycle:

```text
staging
   ↓
evaluation
   ↓
production
   ↓
archived
```

Do not overwrite a production model without preserving its version.

## GPU

The TorchScript loader automatically selects:

```text
CUDA if available
CPU otherwise
```

Production Kubernetes deployment can later expose an NVIDIA GPU to the Expert 1 worker.

## No hallucination rule

This step deliberately does not claim that any disease/pest is detectable.

Actual disease/pest classes, labels, thresholds, preprocessing, and output decoding must come from:

```text
actual Expert 1 dataset
+
actual supplied trained model
+
model documentation/checkpoint metadata
```

The package provides the integration boundary and testing framework without inventing those missing facts.
