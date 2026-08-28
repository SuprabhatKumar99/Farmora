import json
from pathlib import Path

def build_output(image_id, crop_id=None, growth_stage=None):
    return {
        "expert_id": "E01",
        "expert_type": "Visual_Health",
        "input": {"image_id": image_id, "crop_id": crop_id, "growth_stage": growth_stage},
        "visual_assessment": {},
        "evidence": []
    }

if __name__ == "__main__":
    print(json.dumps(build_output("IMG001"), indent=2))
