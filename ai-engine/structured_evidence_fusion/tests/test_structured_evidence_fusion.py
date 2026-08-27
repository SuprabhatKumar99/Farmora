from app.evidence_fusion.schemas.models import *
from app.evidence_fusion.services.fusion_service import StructuredEvidenceFusionService

def make(eid,expert,etype,finding,confidence):
    return EvidenceItem(evidence_id=eid,expert=expert,evidence_type=etype,finding=finding,confidence=confidence,affected_zone="Z1")

def test_fusion():
    r=StructuredEvidenceFusionService().fuse(EvidenceFusionRequest(
        case_id="C1",
        evidences=[make("E1","EXPERT_1_VISUAL_HEALTH",EvidenceType.VISUAL_HEALTH," present ",.9)]
    ))
    assert r.status=="COMPLETED"
    assert r.evidence[0].finding=="present"

def test_conflict():
    r=StructuredEvidenceFusionService().fuse(EvidenceFusionRequest(
        case_id="C1",
        evidences=[
            make("E1","EXPERT_1_VISUAL_HEALTH",EvidenceType.VISUAL_HEALTH,"present",.9),
            make("E2","EXPERT_4_WHOLE_CROP_HEALTH",EvidenceType.WHOLE_CROP_HEALTH,"absent",.7)
        ]
    ))
    assert len(r.conflicts)==1

def test_missing():
    r=StructuredEvidenceFusionService().fuse(EvidenceFusionRequest(case_id="C1"))
    assert len(r.missing_evidence)==7
