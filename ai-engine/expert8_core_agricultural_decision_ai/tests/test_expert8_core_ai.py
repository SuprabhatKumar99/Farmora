from app.expert8_core_ai.services.decision_service import Expert8DecisionService
from app.expert8_core_ai.schemas.models import DecisionStatus


CONTEXT = {
    "evidence": [
        {
            "evidence_id": "E1",
            "expert": "EXPERT_1_VISUAL_HEALTH",
            "evidence_type": "VISUAL_HEALTH",
            "finding": "example",
            "confidence": 0.8,
        }
    ],
    "confidence_summary": {},
    "conflicts": [],
    "missing_evidence": [],
    "context": {"evidence_count": 1},
}


class FakeModel:
    name = "fake-expert8"
    version = "test-1"

    def metadata(self):
        return {"name": self.name, "version": self.version}

    def predict(self, prompt):
        return '''{
          "diagnosis": "TEST_ONLY",
          "likely_cause": null,
          "disease_pest_risk": null,
          "severity": null,
          "affected_zone": null,
          "confidence": 0.5,
          "prevention": [],
          "management": [],
          "treatment_recommendation": [],
          "expert_or_lab_validation_required": true,
          "reasoning_evidence_ids": ["E1"]
        }'''


def test_expert8_decision_flow():
    service = Expert8DecisionService(FakeModel())
    result = service.decide("CASE-1", CONTEXT)

    assert result.status == DecisionStatus.VALIDATION_REQUIRED
    assert result.decision.diagnosis == "TEST_ONLY"
    assert result.decision.reasoning_evidence_ids == ["E1"]


def test_model_required():
    service = Expert8DecisionService()
    result = service.decide("CASE-1", CONTEXT)

    assert result.status == DecisionStatus.FAILED
    assert result.error_code == "MODEL_NOT_LOADED"


def test_incomplete_context():
    service = Expert8DecisionService(FakeModel())
    result = service.decide("CASE-1", {"evidence": []})

    assert result.status == DecisionStatus.FAILED
    assert result.error_code == "INVALID_MODEL_OUTPUT_OR_CONTEXT"
