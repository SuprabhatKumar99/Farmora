from collections import defaultdict
from app.evidence_fusion.schemas.models import EvidenceItem

class ConfidenceScorer:
    def summarize(self, items: list[EvidenceItem]) -> dict:
        groups = defaultdict(list)
        for item in items:
            groups[item.expert].append(item.confidence)
        return {
            expert: {
                "count": len(values),
                "max_confidence": max(values),
                "mean_confidence": sum(values)/len(values),
            }
            for expert, values in groups.items()
        }
