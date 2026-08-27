# STEP 19 — Follow-up & Feedback Loop

This package adds **STEP 19 — Follow-up & Feedback Loop** while preserving
the established project structure from Steps 1–18.

No previous expert, evidence-fusion, Expert 8, decision-output, or validation
directory is renamed or removed.

## Architecture position

```text
Step 1–7 Knowledge / Farm / Monitoring / Analytics
                    ↓
              Experts 1–7
                    ↓
          Structured Evidence Fusion
                    ↓
                Expert 8
                    ↓
       Decision / Risk / Recommendation
                    ↓
        Validation & Ground Truth
                    ↓
              Farmer / Extension
                    ↓
         ┌────────────────────────┐
         │ STEP 19                │
         │ Follow-up & Feedback   │
         │                        │
         │ New Image / Video      │
         │ Field Observation      │
         │ Treatment Outcome      │
         │ Expert Result          │
         │ Laboratory Result      │
         │ Case Correction        │
         └────────────┬───────────┘
                      ↓
              Outcome Comparison
                      ↓
        Validated Learning Candidates
              ↙               ↘
      Knowledge Update      Model Feedback
              ↓               ↓
       Review / Approval   Review / Evaluation
              └───────┬───────┘
                      ↓
             Knowledge / Model
                improvement
```

# 1. Purpose

Step 19 closes the operational feedback loop.

The system records what happens after an AI decision:

```text
Initial case
    ↓
AI decision
    ↓
Recommendation / advisory
    ↓
Follow-up
    ↓
New observation / outcome
    ↓
Validation
    ↓
Error or confirmation analysis
    ↓
Reviewable learning candidate
```

The key rule is:

**Follow-up feedback is evidence for validation and improvement; it is not
automatically treated as truth.**

# 2. Follow-up case

A follow-up case stores:

```text
case_id
original_decision_id
original_model_name
original_model_version
created_at
status
follow_up_due_at
original_evidence_ids
original_recommendation_ids
feedback_ids
```

This connects the future observation to the exact original decision.

# 3. Follow-up lifecycle

```text
CREATED
   ↓
SCHEDULED
   ↓
OBSERVATION_RECEIVED
   ↓
OUTCOME_RECORDED
   ↓
VALIDATED
   ↓
CLOSED
```

A case can also be closed when appropriate without passing through every state.

Invalid state transitions are rejected.

# 4. Feedback types

The implementation supports:

```text
FOLLOW_UP_OBSERVATION
TREATMENT_OUTCOME
FIELD_OBSERVATION
EXPERT_RESULT
LAB_RESULT
CASE_CORRECTION
```

These are categories, not assumptions about the content.

# 5. Feedback record

Each feedback record contains:

```text
feedback_id
case_id
feedback_type
observed_at
source_id
source_type
observation
verified
reviewer_ids
notes
```

The system deliberately stores the source and verification state.

# 6. New image / video feedback

A new image or video should enter the existing observation pipeline rather
than bypassing it:

```text
New Image / Video
       ↓
Step 4 Observation Pipeline
       ↓
Relevant Expert(s)
       ↓
Evidence Fusion
       ↓
Expert 8
       ↓
Updated Decision
       ↓
Step 19 Follow-up Comparison
```

Step 19 does not duplicate image/video processing.

# 7. Environment / sensor feedback

New sensor or environmental information should enter the established
environment pipeline:

```text
New Sensor Data
      ↓
Step 5 Environment & Sensor Pipeline
      ↓
Expert 5 / Other Relevant Experts
      ↓
Evidence Fusion
      ↓
Expert 8
      ↓
Follow-up Comparison
```

Step 19 stores the resulting feedback linkage.

# 8. Remote-sensing feedback

Remote-sensing follow-up should use the existing Step 6 pipeline:

```text
New Drone / Satellite Observation
             ↓
Remote Sensing Pipeline
             ↓
Farm Analytics / Relevant Expert
             ↓
Evidence Fusion
             ↓
Expert 8
             ↓
Follow-up
```

Step 19 is the case/outcome layer, not a replacement for remote-sensing
processing.

# 9. Treatment outcome

Treatment outcome should be recorded only from an actual follow-up observation
or verified source.

The system must not infer:

```text
treatment worked
```

just because a later value changed.

A change in an observation is recorded as a change.

Causal efficacy requires a separate validated evaluation methodology.

# 10. Outcome comparison

The comparator checks explicitly supplied fields.

Example:

```text
Original:
severity = HIGH

Follow-up:
severity = MODERATE

Result:
severity changed from HIGH to MODERATE
```

This does NOT automatically mean:

```text
treatment caused improvement
```

The comparator records the observed difference without inventing causality.

# 11. Mathematical boundary

For a field x:

```text
change(x) = follow_up(x) - original(x)
```

only when x is numeric and the project explicitly defines the subtraction as
meaningful.

For categorical values:

```text
changed(x) =
    0, if follow_up(x) == original(x)
    1, otherwise
```

The current implementation performs categorical equality comparison and stores
the before/after values.

It does not calculate unsupported efficacy percentages.

# 12. Verification

Feedback can be:

```text
verified = false
```

or:

```text
verified = true
```

Only verified feedback is eligible to generate learning candidates.

Verification requires the project's actual review process.

Step 19 does not declare a laboratory or field observation correct merely
because it was submitted.

# 13. Ground truth relationship

Step 18 remains authoritative for ground-truth validation.

Step 19 can produce new evidence that may later enter the ground-truth
workflow:

```text
Follow-up Feedback
       ↓
Review
       ↓
Ground Truth Candidate
       ↓
Step 18 Validation / Verification
       ↓
Verified Ground Truth
```

The feedback loop does not bypass Step 18.

# 14. Knowledge-base update boundary

Verified feedback can create:

```text
KNOWLEDGE_UPDATE_CANDIDATE
```

The candidate contains:

```text
case_id
source_feedback_ids
source_evidence_ids
payload
requires_review = true
```

It is NOT directly written into the production knowledge base.

Correct flow:

```text
Verified Feedback
      ↓
Candidate
      ↓
Human / Qualified Review
      ↓
Approved Knowledge Update
      ↓
Knowledge Base
```

# 15. Model feedback boundary

Verified feedback can also create:

```text
MODEL_FEEDBACK_CANDIDATE
```

The candidate records:

```text
original model name
original model version
feedback type
observation
source feedback ID
```

It does not automatically retrain the model.

Correct flow:

```text
Verified Feedback
      ↓
Model Feedback Candidate
      ↓
Dataset Review
      ↓
Training / Fine-tuning
      ↓
Evaluation
      ↓
Step 18 Validation
      ↓
New Model Version
```

# 16. No automatic self-training

The implementation intentionally does NOT perform:

```text
feedback → automatic model weight update
```

and does NOT perform:

```text
feedback → automatic knowledge-base modification
```

This prevents unverified field observations from silently changing the
system.

# 17. Evidence traceability

Every follow-up case retains:

```text
original_evidence_ids
original_recommendation_ids
original_decision_id
original_model_name
original_model_version
```

Feedback retains:

```text
feedback_id
source_id
reviewer_ids
verification state
```

This allows an outcome to be traced back to the original AI decision.

# 18. Model version traceability

Suppose:

```text
Original decision:
model = agricultural-decision-ai
version = 1.4
```

A later model may be:

```text
version = 1.5
```

The follow-up record still identifies the original model as:

```text
1.4
```

This is important for retrospective model evaluation.

# 19. API

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:

```text
POST /api/v1/followup-feedback/cases
POST /api/v1/followup-feedback/cases/{case_id}/feedback
POST /api/v1/followup-feedback/cases/{case_id}/compare
GET  /api/v1/followup-feedback/cases/{case_id}/learning-candidates
GET  /api/v1/followup-feedback/health
```

# 20. Create follow-up case

Example:

```json
{
  "case_id": "CASE-001",
  "original_decision_id": "DECISION-001",
  "original_model_name": "agricultural-decision-ai",
  "original_model_version": "1.0",
  "created_at": "2026-08-27T00:00:00Z",
  "follow_up_due_at": null,
  "original_evidence_ids": ["E1", "E2"],
  "original_recommendation_ids": ["REC-001"]
}
```

These are API examples only.

# 21. Add feedback

Example:

```json
{
  "feedback_id": "FEEDBACK-001",
  "case_id": "CASE-001",
  "feedback_type": "FIELD_OBSERVATION",
  "observed_at": "2026-09-03T00:00:00Z",
  "source_id": "FIELD-OBS-001",
  "source_type": "FIELD",
  "observation": {
    "severity": "MODERATE"
  },
  "verified": false,
  "reviewer_ids": [],
  "notes": null
}
```

Unverified feedback remains unverified.

# 22. Compare outcome

The comparison endpoint accepts the original decision fields:

```json
{
  "severity": "HIGH",
  "diagnosis": "example"
}
```

It compares these with explicitly supplied follow-up observations.

The output identifies:

```text
before
after
field
feedback_id
```

# 23. Learning candidates

After verified feedback is recorded:

```text
GET /api/v1/followup-feedback/cases/{case_id}/learning-candidates
```

can return:

```text
knowledge_candidates
model_feedback_candidates
```

Every candidate has:

```text
requires_review = true
```

# 24. Dataset

```text
data/crop_health_dataset/
└── 19_followup_feedback_loop/
    ├── followup_cases.csv
    ├── feedback_records.csv
    └── README.md
```

The included records are structural examples only.

# 25. Testing

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run:

```bash
pytest -q
```

Validate dataset structure:

```bash
python scripts/validate_step19_dataset.py
```

# 26. Test cases included

The tests verify:

```text
follow-up case creation
feedback recording
outcome comparison
unverified feedback exclusion
verified feedback candidate creation
evidence/model traceability
```

# 27. Event architecture

The event definitions support the future Kafka integration:

```text
followup.created
followup.scheduled
followup.feedback.received
followup.outcome.recorded
followup.validation.completed
followup.learning.candidate.created
```

The current package defines the event contract but does not force Kafka into
Step 19's local implementation.

The established backend/Kafka architecture can publish these events when the
platform integration stage is connected.

# 28. Recommended asynchronous production flow

```text
Spring Boot
     ↓
Kafka
     ↓
Follow-up Event
     ↓
AI / Follow-up Worker
     ↓
Observation Pipeline
     ↓
Experts
     ↓
Evidence Fusion
     ↓
Expert 8
     ↓
Decision Outputs
     ↓
Follow-up Comparison
     ↓
Validation
```

# 29. Notification boundary

The actual farmer notification belongs to the platform/backend layer.

Step 19 determines follow-up state and records feedback.

It should not directly own:

```text
SMS
WhatsApp
push notifications
email
```

Those remain application/integration responsibilities.

# 30. Storage boundary

The current implementation uses an in-memory store so it can be tested
independently.

Production persistence should be handled through the existing backend data
architecture.

Do not add a second independent PostgreSQL database for Step 19.

# 31. Follow-up with new images

A proper end-to-end case is:

```text
Initial Image
    ↓
Expert 1–7
    ↓
Evidence Fusion
    ↓
Expert 8
    ↓
Step 17
    ↓
Initial Decision
    ↓
Follow-up Case
    ↓
New Image
    ↓
Step 4
    ↓
Expert inference
    ↓
New Evidence
    ↓
New Decision
    ↓
Step 19 Comparison
```

# 32. Follow-up with laboratory result

```text
Initial AI Decision
       ↓
Follow-up Case
       ↓
Laboratory Result
       ↓
Feedback Record
       ↓
Qualified Review
       ↓
Verified Feedback
       ↓
Step 18 Ground Truth Workflow
       ↓
Model / Knowledge Evaluation
```

A lab result should not be fabricated or inferred from an AI prediction.

# 33. Follow-up with expert field validation

```text
AI Decision
    ↓
Extension / Qualified Expert
    ↓
Field Observation
    ↓
Feedback Record
    ↓
Review
    ↓
Verified Feedback
```

The project-specific qualification and review process must define who can
validate the result.

# 34. Error-analysis loop

```text
Prediction
    ↓
Follow-up
    ↓
Verified Outcome
    ↓
Compare
    ↓
Mismatch
    ↓
Failure Case
    ↓
Dataset Candidate
    ↓
Model Evaluation
```

This provides the bridge between operational deployment and model improvement.

# 35. Knowledge improvement loop

```text
Verified Follow-up
       ↓
Knowledge Candidate
       ↓
Review
       ↓
Approved
       ↓
Crop / Disease / Local Knowledge
       ↓
Knowledge Base
```

No direct automatic write is performed.

# 36. Model improvement loop

```text
Verified Follow-up
       ↓
Model Feedback Candidate
       ↓
Dataset Curation
       ↓
Training / Fine-tuning
       ↓
Evaluation
       ↓
Validation & Ground Truth
       ↓
New Model Version
```

The exact training method depends on the Expert/model being improved.

# 37. Data quality rules

Follow-up data should preserve:

```text
case identity
observation timestamp
source
zone/farm context where available
model version
original decision
new observation
verification status
reviewer
```

Only fields actually available should be recorded.

# 38. No causal hallucination

The feedback loop must distinguish:

```text
Observed change
```

from:

```text
Cause of change
```

For example:

```text
severity decreased
```

does not automatically prove:

```text
recommended treatment caused the decrease
```

Causal claims require an appropriate evaluation design and supporting data.

# 39. No ground-truth hallucination

The system must never transform:

```text
farmer report
```

into:

```text
verified ground truth
```

without the defined validation/review process.

# 40. Final architecture

```text
                         ORIGINAL CASE
                              ↓
                     Experts 1–7
                              ↓
                    Evidence Fusion
                              ↓
                         Expert 8
                              ↓
                 Decision/Risk/Advice
                              ↓
                   Validation/Ground Truth
                              ↓
                    Farmer / Extension
                              ↓
                    ┌─────────────────┐
                    │ STEP 19         │
                    │ FOLLOW-UP        │
                    └────────┬────────┘
                             ↓
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
          New Image       Sensor         Field/Lab
          / Video         Data           Feedback
              ↓              ↓              ↓
          Existing       Existing        Review
          Pipeline       Pipeline           ↓
              └──────────────┼──────────────┘
                             ↓
                       New Evidence
                             ↓
                       New Decision
                             ↓
                     Outcome Comparison
                             ↓
                         Validation
                             ↓
                  ┌──────────┴──────────┐
                  ↓                     ↓
           Knowledge Candidate     Model Candidate
                  ↓                     ↓
                Review                Review
                  ↓                     ↓
            Knowledge Base       Training/Evaluation
```

# 41. Not included

```text
Automatic model retraining
Automatic knowledge-base modification
Automatic ground-truth creation
Automatic causal-effect estimation
Notification provider
Kafka implementation
PostgreSQL implementation
Farmer UI
Extension UI
```

These remain separate concerns of the surrounding architecture.

# 42. Final principle

The complete feedback loop is:

```text
Observe
  ↓
Decide
  ↓
Act
  ↓
Follow Up
  ↓
Observe Outcome
  ↓
Verify
  ↓
Compare
  ↓
Learn Candidate
  ↓
Review
  ↓
Improve Knowledge / Model
  ↓
Re-validate
```

The critical boundary is:

```text
Feedback ≠ Ground Truth
Feedback → Validation → Verified Evidence → Learning Candidate
```

This prevents the system from silently learning from incorrect, incomplete,
or unverified field feedback.
