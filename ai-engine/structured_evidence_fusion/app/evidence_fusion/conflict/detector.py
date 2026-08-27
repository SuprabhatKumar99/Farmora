from collections import defaultdict
from app.evidence_fusion.schemas.models import EvidenceConflict, EvidenceItem

class ConflictDetector:
    OPPOSITES = {
        ("present","absent"), ("healthy","unhealthy"),
        ("normal","abnormal"), ("detected","not_detected"),
    }

    def detect(self, items: list[EvidenceItem]) -> list[EvidenceConflict]:
        groups=defaultdict(list)
        for item in items:
            groups[(item.evidence_type, item.affected_zone)].append(item)
        out=[]; n=1
        for group in groups.values():
            for i,a in enumerate(group):
                for b in group[i+1:]:
                    x,y=a.finding.lower().strip(),b.finding.lower().strip()
                    if (x,y) in self.OPPOSITES or (y,x) in self.OPPOSITES:
                        out.append(EvidenceConflict(
                            conflict_id=f"CONFLICT-{n:04d}",
                            evidence_ids=[a.evidence_id,b.evidence_id],
                            conflict_type="EXPLICIT_OPPOSITE_FINDING",
                            description=f"Explicitly opposing findings: '{a.finding}' vs '{b.finding}'."
                        ))
                        n+=1
        return out
