from app.decision_outputs.schemas.models import (
    DecisionRecommendationOutput,
)


class DecisionSerializer:
    def to_dict(self, result: DecisionRecommendationOutput) -> dict:
        return result.model_dump(mode="json")
