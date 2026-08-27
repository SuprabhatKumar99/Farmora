# STEP 15 — Structured Evidence Fusion

This step adds the structured evidence-fusion layer **without changing the
existing Expert 1–7 structure**.

## Architecture

```text
Expert 1 ─┐
Expert 2 ─┤
Expert 3 ─┤
Expert 4 ─┤
Expert 5 ─┤
Expert 6 ─┤
Expert 7 ─┘
           ↓
Structured Evidence Fusion
           ↓
Expert 8 — Core Agricultural Decision LLM
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
└── evidence_fusion/
    ├── api/
    ├── schemas/
    ├── services/
    ├── normalization/
    ├── conflict/
    ├── completeness/
    ├── scoring/
    ├── context/
    └── storage/
```

## Responsibilities

The fusion layer performs exactly the operations defined in the architecture:

```text
Collect expert outputs
        ↓
Normalize evidence
        ↓
Compare confidence
        ↓
Detect contradictions
        ↓
Identify missing evidence
        ↓
Build final structured context
```

It does **not** make the final diagnosis or treatment decision.

## Evidence item

```text
evidence_id
expert
evidence_type
finding
confidence
severity
affected_zone
source_ids
model_name
model_version
attributes
```

The seven evidence types map to Experts 1–7.

## Normalization

Current normalization is representation-only:

```text
Whitespace normalization
Confidence bounded to [0,1]
Severity bounded to [0,1]
```

It does not invent meanings or convert arbitrary words into numerical scores.

## Confidence

The implementation reports:

```text
count
maximum confidence
descriptive mean confidence
```

For values c1...cn:

```text
mean(c) = Σci / n
```

This is a descriptive statistic, **not a calibrated probability**. The system
does not assume expert independence or multiply confidence values.

## Conflict detection

Only explicit opposite findings are detected:

```text
present ↔ absent
healthy ↔ unhealthy
normal ↔ abnormal
detected ↔ not_detected
```

The fusion layer does not invent semantic contradictions.

**Conflicts are detected, not silently resolved.**

## Missing evidence

Missing Expert 1–7 outputs are explicitly represented.

Missing evidence is not treated as proof of a negative condition.

## Context

The structured context contains:

```text
evidence_by_type
evidence_by_zone
evidence_count
experts_present
```

This is intended to become part of Expert 8's structured input.

## API

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoint:

```text
POST /api/v1/evidence-fusion/fuse
```

Health:

```text
GET /api/v1/evidence-fusion/health
GET /health
GET /ready
```

Example request:

```json
{
  "case_id": "CASE-001",
  "evidences": [
    {
      "evidence_id": "E1",
      "expert": "EXPERT_1_VISUAL_HEALTH",
      "evidence_type": "VISUAL_HEALTH",
      "finding": "present",
      "confidence": 0.91,
      "affected_zone": "ZONE-1"
    }
  ]
}
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Testing

```bash
pytest -q
python scripts/validate_evidence_fusion_dataset.py
```

## Evidence boundary

Step 15 does not:

```text
diagnose disease
determine root cause
select pesticide
calculate dosage
generate treatment
generate IPM instructions
invent missing evidence
silently resolve expert conflicts
```

It prepares the evidence for Expert 8.

## No-hallucination rule

If evidence is absent, record it as missing.

If experts disagree, record the conflict.

If confidence semantics are unknown, preserve the supplied value without
pretending it is a calibrated probability.

No agricultural conclusion is invented by this layer.

## Not included

```text
Expert 8
Final crop-health decision
Final farmer advisory
Kafka integration
PostgreSQL integration
MLflow lifecycle
```

Those remain subsequent implementation stages.
