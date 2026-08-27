from app.evidence_fusion.schemas.models import EvidenceItem, MissingEvidence

class EvidenceCompletenessChecker:
    EXPECTED = {
        "EXPERT_1_VISUAL_HEALTH":"VISUAL_HEALTH",
        "EXPERT_2_CHEMICAL_PESTICIDE_DAMAGE":"CHEMICAL_PESTICIDE_DAMAGE",
        "EXPERT_3_ROOT_INTERNAL_HEALTH":"ROOT_INTERNAL_HEALTH",
        "EXPERT_4_WHOLE_CROP_HEALTH":"WHOLE_CROP_HEALTH",
        "EXPERT_5_ENVIRONMENT_WEATHER":"ENVIRONMENT_WEATHER",
        "EXPERT_6_PREVENTION_IPM":"PREVENTION_IPM",
        "EXPERT_7_TREATMENT_MANAGEMENT":"TREATMENT_MANAGEMENT",
    }
    def check(self, items: list[EvidenceItem]) -> list[MissingEvidence]:
        present={x.expert for x in items}
        return [
            MissingEvidence(evidence_type=t, reason="No evidence item was supplied by this expert.")
            for expert,t in self.EXPECTED.items() if expert not in present
        ]
