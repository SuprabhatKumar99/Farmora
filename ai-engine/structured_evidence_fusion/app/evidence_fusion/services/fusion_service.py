from app.evidence_fusion.schemas.models import EvidenceFusionRequest, FusedEvidenceContext
from app.evidence_fusion.normalization.normalizer import EvidenceNormalizer
from app.evidence_fusion.scoring.confidence import ConfidenceScorer
from app.evidence_fusion.conflict.detector import ConflictDetector
from app.evidence_fusion.completeness.checker import EvidenceCompletenessChecker
from app.evidence_fusion.context.builder import EvidenceContextBuilder

class StructuredEvidenceFusionService:
    def __init__(self):
        self.normalizer=EvidenceNormalizer()
        self.scorer=ConfidenceScorer()
        self.conflict_detector=ConflictDetector()
        self.completeness_checker=EvidenceCompletenessChecker()
        self.context_builder=EvidenceContextBuilder()

    def fuse(self, request: EvidenceFusionRequest) -> FusedEvidenceContext:
        evidence=self.normalizer.normalize(request.evidences)
        return FusedEvidenceContext(
            case_id=request.case_id,
            evidence=evidence,
            confidence_summary=self.scorer.summarize(evidence),
            conflicts=self.conflict_detector.detect(evidence),
            missing_evidence=self.completeness_checker.check(evidence),
            context=self.context_builder.build(evidence),
            status="COMPLETED",
        )
