def collect_evidence_ids(decision) -> list[str]:
    """Return unique evidence IDs in stable order."""
    seen = set()
    output = []

    for evidence_id in decision.reasoning_evidence_ids:
        if evidence_id and evidence_id not in seen:
            seen.add(evidence_id)
            output.append(evidence_id)

    return output
