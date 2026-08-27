# STEP 9 — Expert 2: Chemical/Pesticide Damage

Additive implementation. Do not rename/remove previous project components.

## Structure
```text
app/experts/expert2_chemical_pesticide_damage/
├── api/
├── schemas/
├── services/
├── preprocessing/
├── inference/
├── postprocessing/
├── models/
└── storage/

crop_health_dataset/
└── 09_expert2_chemical_pesticide_damage/
    ├── expert2_observations.csv
    └── expert2_labels.csv
```

## Pipeline
```text
Image/Observation
 → validation/decode
 → model-specific preprocessing
 → supplied trained model
 → prediction
 → post-processing
 → structured Expert 2 evidence
```

Expert 2 produces evidence for possible chemical/pesticide damage patterns. It does not independently prescribe chemicals, determine dose, or make the final diagnosis.

## Supplied model
No trained model is fabricated. A TorchScript loader is provided:

```text
models/expert2_chemical_pesticide_damage/production/
```

Test:
```bash
python scripts/test_expert2.py <model.pt> <image.jpg>
```

The exact input resolution, normalization, RGB/BGR convention, tensor layout, class mapping, output format, NMS, and segmentation decoding must match the supplied model. They are intentionally not guessed.

## Model candidates
If image-level labels: EfficientNet, ConvNeXt, ViT/DeiT.
If localized damage: YOLO family, RT-DETR.
If pixel masks: U-Net, DeepLab, Mask R-CNN, YOLO segmentation variants.

Choose only after evaluating the actual dataset. Measure precision, recall, F1, false-negative rate, mAP for detection, IoU/Dice for segmentation, latency, and GPU memory.

## Testing
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Run API:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:
```text
POST /api/v1/experts/expert2/chemical-pesticide-damage/analyze
GET  /api/v1/experts/expert2/chemical-pesticide-damage/model
GET  /health
GET  /ready
```

## Important boundary
```text
Expert 1 + Expert 2 + Experts 3–7
              ↓
     Structured Evidence Fusion
              ↓
           Expert 8
              ↓
     Final Crop Health Decision
```

No disease-specific causal claims, pesticide-dose rules, treatment recommendations, or agricultural thresholds are fabricated here. Those require verified knowledge/data and later decision layers.
