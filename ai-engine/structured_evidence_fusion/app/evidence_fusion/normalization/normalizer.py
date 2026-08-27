from app.evidence_fusion.schemas.models import EvidenceItem

class EvidenceNormalizer:
    def normalize(self, items: list[EvidenceItem]) -> list[EvidenceItem]:
        return [
            item.model_copy(update={
                "finding": " ".join(item.finding.strip().split()),
                "confidence": min(max(item.confidence, 0.0), 1.0),
                "severity": None if item.severity is None else min(max(item.severity, 0.0), 1.0),
            })
            for item in items
        ]
