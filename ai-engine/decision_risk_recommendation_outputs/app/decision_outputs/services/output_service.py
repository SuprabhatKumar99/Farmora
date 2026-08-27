from app.decision_outputs.schemas.models import (
    DecisionOutputRequest,
    DecisionRecommendationOutput,
)
from app.decision_outputs.risk.assessor import RiskAssessor
from app.decision_outputs.recommendations.builder import RecommendationBuilder
from app.decision_outputs.validation.output_validator import DecisionOutputValidator
from app.decision_outputs.traceability.trace import collect_evidence_ids


class DecisionRiskRecommendationService:
    """Build the externally consumable Step 17 output from Expert 8.

    Step 17 is an output-contract layer. It formats and validates the
    decision; it does not independently diagnose the crop or invent treatment.
    """

    def __init__(self):
        self.risk_assessor = RiskAssessor()
        self.recommendation_builder = RecommendationBuilder()
        self.validator = DecisionOutputValidator()

    def build(self, request: DecisionOutputRequest):
        decision = request.decision
        evidence_ids = collect_evidence_ids(decision)

        risk = self.risk_assessor.assess(
            decision.disease_pest_risk,
            decision.confidence,
            evidence_ids,
        )

        recommendations = self.recommendation_builder.build(
            decision,
            request.model_version,
        )

        result = DecisionRecommendationOutput(
            case_id=request.case_id,
            diagnosis=decision.diagnosis,
            likely_cause=decision.likely_cause,
            affected_zone=decision.affected_zone,
            risk=risk,
            recommendations=recommendations,
            validation_required=(
                decision.expert_or_lab_validation_required
            ),
            evidence_ids=evidence_ids,
            model_name=request.model_name,
            model_version=request.model_version,
            status="VALIDATION_REQUIRED",
        )

        return self.validator.validate(result, decision)
