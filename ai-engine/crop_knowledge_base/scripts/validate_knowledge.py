import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.knowledge.repository import CropKnowledgeRepository
from app.knowledge.validator import CropKnowledgeValidator

base = Path(__file__).resolve().parents[1] / "data/crop_health_dataset/01_crop_knowledge"
repo = CropKnowledgeRepository(base)
CropKnowledgeValidator().validate(repo)

print("Knowledge base validation: PASS")
print(f"Crops: {len(repo.crops)}")
print(f"Varieties: {len(repo.varieties)}")
print(f"Growth stages: {len(repo.growth_stages)}")
print(f"Lifecycle records: {len(repo.crop_lifecycle)}")
print(f"Requirement records: {len(repo.crop_requirements)}")
