from collections import defaultdict
from app.evidence_fusion.schemas.models import EvidenceItem

class EvidenceContextBuilder:
    def build(self, items: list[EvidenceItem]) -> dict:
        by_type=defaultdict(list); by_zone=defaultdict(list)
        for x in items:
            by_type[x.evidence_type.value].append(x.evidence_id)
            if x.affected_zone:
                by_zone[x.affected_zone].append(x.evidence_id)
        return {
            "evidence_by_type":dict(by_type),
            "evidence_by_zone":dict(by_zone),
            "evidence_count":len(items),
            "experts_present":sorted({x.expert for x in items}),
        }
