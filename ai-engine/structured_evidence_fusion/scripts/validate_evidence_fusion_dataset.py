from pathlib import Path
import csv
base=Path(__file__).resolve().parents[1]/"data/crop_health_dataset/15_structured_evidence_fusion"
for name in ["evidence_fusion_cases.csv","evidence_fusion_output.csv"]:
    p=base/name
    if not p.exists(): raise FileNotFoundError(p)
    with p.open(encoding="utf-8") as f:
        if len(list(csv.reader(f)))<2: raise ValueError(f"{name} is empty")
print("Structured evidence fusion dataset validation: PASS")
