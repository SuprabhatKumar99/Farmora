# STEP 16 — Expert 8: Core Agricultural Decision AI

This package adds **STEP 16 — Expert 8: Core Agricultural Decision AI**
without changing or replacing the established Expert 1–7 and Structured
Evidence Fusion structure.

## Position in the final AI architecture

```text
Expert 1 — Visual Health
Expert 2 — Chemical/Pesticide Damage
Expert 3 — Root/Internal Health
Expert 4 — Whole Crop Health
Expert 5 — Environment & Weather
Expert 6 — Prevention / IPM
Expert 7 — Treatment / Management
             ↓
Structured Evidence Fusion
             ↓
┌────────────────────────────────────────────┐
│ EXPERT 8 — CORE AGRICULTURAL DECISION AI  │
│                                            │
│ Agricultural Decision LLM                  │
│ Evidence Synthesis                         │
│ Conflict Resolution                        │
│ Missing-Evidence Reasoning                 │
│ Risk Assessment                            │
│ Decision Generation                        │
└──────────────────────┬─────────────────────┘
                       ↓
             Final Crop Health Decision
```

## Project structure

The established structure remains intact:

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
│
└── expert8_core_ai/
    ├── api/
    ├── schemas/
    ├── services/
    ├── preprocessing/
    ├── inference/
    ├── postprocessing/
    ├── models/
    ├── prompting/
    ├── validation/
    └── storage/
```

No previous expert directory is renamed or removed.

## Why Expert 8 is separate

Expert 8 is not another computer-vision expert.

Experts 1–7 generate domain-specific evidence.

Step 15 structures that evidence.

Expert 8 consumes the structured evidence and performs the final agricultural
decision reasoning.

```text
Experts 1–7
    ↓
Evidence Fusion
    ↓
Structured Evidence
    ↓
Prompt / Model Input
    ↓
Expert 8
    ↓
Structured Decision
```

## Core responsibilities

Expert 8 is responsible for:

```text
Evidence synthesis
Expert conflict reasoning
Missing-evidence reasoning
Disease/pest reasoning
Risk assessment
Severity assessment
Decision generation
Confidence reporting
Validation/abstention decision
```

It is not responsible for collecting raw images, raw sensor streams, or
directly accessing PostgreSQL.

## Input

Expert 8 consumes the Step 15 structured evidence context:

```text
evidence
confidence_summary
conflicts
missing_evidence
context
```

The model is therefore not expected to independently reconstruct the entire
farm state from raw modalities.

## Input flow

```text
Expert 1 output ─┐
Expert 2 output ─┤
Expert 3 output ─┤
Expert 4 output ─┤
Expert 5 output ─┤
Expert 6 output ─┤
Expert 7 output ─┘
                  ↓
       Structured Evidence Fusion
                  ↓
          Evidence Context
                  ↓
         Expert 8 Preprocessor
                  ↓
             Prompt Builder
                  ↓
            Decision LLM
```

# 1. Model architecture

The project specification calls for:

```text
Agricultural Decision LLM
1–3 billion parameters
```

This package does **not** claim that a particular 1–3B model is trained,
fine-tuned, or included.

The actual supplied model remains the source of truth.

The implementation supports a local Hugging Face-compatible causal language
model through `transformers`.

## Recommended model selection

For a 1–3B parameter agricultural decision model, the exact base model should
be selected only after checking:

```text
license
language support
context length
available training data
fine-tuning support
GPU/RAM constraints
instruction-following quality
structured JSON reliability
benchmark performance
agricultural-domain evaluation
```

Do not select a model solely because it has the correct parameter count.

The supplied/trained model should be loaded through the adapter.

# 2. Model lifecycle

```text
models/
└── expert8_core_ai/
    ├── production/
    ├── staging/
    └── archived/
```

Place the supplied Hugging Face-compatible model directory under:

```text
models/expert8_core_ai/production/
```

The directory should contain the files required by the model/tokenizer,
for example the configuration, tokenizer and model weights appropriate to
the supplied artifact.

## Model version

Every result contains:

```text
model_name
model_version
```

This is required for auditability.

# 3. Inference module

Unlike an empty placeholder, Expert 8 has a real inference layer:

```text
inference/
├── inference_engine.py
└── output_parser.py
```

Responsibilities:

```text
inference_engine.py
    Execute the loaded decision model.

output_parser.py
    Parse the model response into structured JSON.
```

The actual execution flow is:

```text
Structured Evidence Context
        ↓
Prompt Builder
        ↓
Inference Engine
        ↓
Local Causal LM
        ↓
Raw Generated Output
        ↓
Output Parser
        ↓
Decision Validator
        ↓
Decision Result
```

# 4. Preprocessing

`preprocessing/context.py` validates that the fusion context contains:

```text
evidence
confidence_summary
conflicts
missing_evidence
context
```

It does not create missing evidence.

# 5. Prompting

The prompt builder provides the model with the structured evidence.

The system instruction explicitly requires:

```text
Use supplied evidence
Do not invent missing observations
Do not invent causes
Do not invent diagnosis
Do not invent treatment instructions
Preserve uncertainty
Respect conflicts
Request validation when necessary
```

The prompt builder does not add agricultural facts.

# 6. Evidence guard

Before inference, the evidence guard verifies that the model has a structured
fusion context.

This prevents accidentally calling Expert 8 with an unrelated or incomplete
payload.

# 7. Output schema

The intended final decision structure is:

```text
Diagnosis / Likely diagnosis
Likely cause
Disease / pest risk
Severity
Affected zone
Confidence
Prevention
Management
Treatment recommendation
Expert / laboratory validation required
Reasoning evidence IDs
```

Example schema:

```json
{
  "diagnosis": null,
  "likely_cause": null,
  "disease_pest_risk": null,
  "severity": null,
  "affected_zone": null,
  "confidence": null,
  "prevention": [],
  "management": [],
  "treatment_recommendation": [],
  "expert_or_lab_validation_required": true,
  "reasoning_evidence_ids": []
}
```

The `null` and empty values are intentional examples, not fabricated
agricultural conclusions.

# 8. Decision status

Expert 8 supports:

```text
COMPLETED
NEED_MORE_DATA
VALIDATION_REQUIRED
FAILED
```

The current safety-oriented validator defaults validation to required unless
the supplied model explicitly provides the field.

# 9. Conflict reasoning

Step 15 detects conflicts.

Expert 8 receives those conflicts.

Example:

```text
Expert 1 → finding A, confidence 0.90
Expert 4 → finding B, confidence 0.70
              ↓
       Evidence Fusion
              ↓
           CONFLICT
              ↓
          Expert 8
```

Expert 8 must reason from:

```text
finding
confidence
expert identity
model version
affected zone
source IDs
missing evidence
```

The system must not resolve a conflict merely by selecting the highest
confidence number.

# 10. Missing evidence

If Step 15 reports:

```text
missing_evidence:
    ROOT_INTERNAL_HEALTH
```

Expert 8 should preserve that limitation.

It must not infer:

```text
root health = normal
```

merely because root evidence is absent.

# 11. Confidence

Expert 8 receives the confidence values generated by the upstream experts and
fusion layer.

No unsupported Bayesian calculation is introduced.

A model's confidence output should be considered meaningful only if the model
has been appropriately evaluated/calibrated.

# 12. Treatment boundary

Expert 8 may receive Expert 7 treatment/management candidates.

It must not invent:

```text
pesticide
active ingredient
dosage
application rate
spray concentration
waiting period
pre-harvest interval
tank mixture
```

Concrete treatment information must originate from verified project knowledge
and validated model outputs.

If evidence is insufficient:

```text
request additional evidence
or
require expert/laboratory validation
```

# 13. No direct database access

Expert 8 follows the established AI-engine boundary:

```text
Spring Boot
     ↓
AI Gateway / Kafka
     ↓
AI Engine
     ↓
Expert 8
```

Expert 8 does not directly access:

```text
PostgreSQL
Redis
Frontend
```

The backend remains responsible for application/business data.

# 14. API

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoint:

```text
POST /api/v1/expert8/core-ai/decide
GET  /api/v1/expert8/core-ai/model
GET  /health
GET  /ready
```

Example request:

```json
{
  "case_id": "CASE-001",
  "evidence_context": {
    "evidence": [],
    "confidence_summary": {},
    "conflicts": [],
    "missing_evidence": [],
    "context": {}
  },
  "model_version": "production"
}
```

The empty evidence values above are only a schema example.

# 15. Testing with your supplied model

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then place your local model in:

```text
models/expert8_core_ai/production/<your-model-directory>/
```

Test:

```bash
python scripts/test_expert8.py     models/expert8_core_ai/production/<your-model-directory>     path/to/evidence-context.json
```

The JSON input must contain:

```json
{
  "case_id": "CASE-001",
  "evidence_context": {
    "evidence": [],
    "confidence_summary": {},
    "conflicts": [],
    "missing_evidence": [],
    "context": {}
  }
}
```

Replace the example context with the actual Step 15 output.

# 16. Unit tests

Run:

```bash
pytest -q
```

The tests use a fake model only to verify:

```text
context validation
prompt/inference flow
output parsing
decision validation
validation-required behavior
model-not-loaded handling
```

They do not represent real agricultural decisions.

# 17. Dataset

```text
data/crop_health_dataset/
└── 16_expert8_core_ai/
    ├── decision_cases.csv
    └── decision_targets.csv
```

The included records are placeholders for structure/testing only.

Validate:

```bash
python scripts/validate_expert8_dataset.py
```

# 18. Training / fine-tuning architecture

Training remains separate from production inference.

```text
Verified Agricultural Data
        ↓
Structured Training Examples
        ↓
Train / Validation / Test
        ↓
Supervised Fine-Tuning
        ↓
Evaluation
        ↓
Safety / Evidence Evaluation
        ↓
Model Registry
        ↓
Production Model
        ↓
Expert 8 Inference
```

Do not train inside the production FastAPI request path.

# 19. Training example concept

A training record should conceptually contain:

```text
INPUT:
Structured Evidence Context

TARGET:
Validated structured decision
```

The target must be created from verified agricultural decisions/data.

Do not use model-generated hallucinations as ground-truth labels without
appropriate validation.

# 20. Evaluation

Evaluate both language-model quality and decision quality.

Recommended categories:

```text
Evidence grounding
Diagnosis accuracy
Cause accuracy
Risk assessment accuracy
Severity accuracy
Zone accuracy
Treatment/management validity
Abstention quality
Conflict resolution
Missing-evidence handling
Structured-output validity
```

Also measure:

```text
JSON validity rate
unsupported-claim rate
evidence-traceability rate
unsafe-recommendation rate
validation/abstention accuracy
```

The exact thresholds must be defined from the project's evaluation protocol;
this package does not invent acceptance thresholds.

# 21. Latency

Track:

```text
preprocessing latency
prompt construction latency
model inference latency
output parsing latency
total decision latency
```

For GPU deployment, also monitor:

```text
GPU utilization
GPU memory
CPU utilization
request queue
model loading time
```

# 22. Hardware

For local inference:

```text
CPU
  ↓
PyTorch / Transformers
  ↓
Causal LM
```

For GPU:

```text
NVIDIA GPU
    ↓
CUDA
    ↓
PyTorch
    ↓
Transformers
    ↓
Agricultural Decision LLM
```

Quantization, ONNX, TensorRT, or other optimization should be introduced only
after baseline accuracy and latency are established and the supplied model
supports the chosen runtime.

# 23. Final output flow

```text
                 Experts 1–7
                      │
                      ▼
          Structured Evidence Fusion
                      │
          ┌───────────┼───────────┐
          │           │           │
       Evidence    Conflicts    Missing
          │           │           │
          └───────────┼───────────┘
                      ▼
               Expert 8 Core AI
                      │
              ┌───────┴────────┐
              ▼                ▼
        High confidence    Low confidence
              │                │
              ▼                ▼
     Prevention / IPM /    Request More Data
     Management Advisory   Expert / Lab Validation
```

# 24. Final architecture boundary

The complete AI reasoning chain is:

```text
Crop Knowledge Base
        ↓
Farm Digital Profile
        ↓
Monitoring / Observation Pipelines
        ↓
Farm Analytics
        ↓
Experts 1–7
        ↓
Structured Evidence Fusion
        ↓
Expert 8 — Core Agricultural Decision AI
        ↓
Final Crop Health Decision
        ↓
Farmer / Extension Platform
        ↓
Follow-up & Feedback
        ↓
Knowledge Base / Model Improvement
```

## No-hallucination rule

Expert 8 is the final reasoning component, but it is still constrained by
evidence.

It must not manufacture:

```text
observations
sensor values
disease evidence
causes
expert findings
laboratory results
treatment facts
pesticide details
confidence
```

When the available evidence does not support a reliable decision, the correct
behavior is to preserve uncertainty and request additional evidence or
expert/laboratory validation.

## Not included in Step 16

```text
Final farmer/extension UI
Spring Boot integration
Kafka integration
PostgreSQL integration
Redis integration
Notification service
Follow-up feedback service
```

Those belong to the surrounding platform/integration stages.
