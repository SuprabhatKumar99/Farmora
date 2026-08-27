import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.knowledge.repository import DiseasePestKnowledgeRepository
from app.knowledge.validator import DiseasePestKnowledgeValidator

base = Path(__file__).resolve().parents[1] / "data/crop_health_dataset/02_disease_pest_knowledge"
repo = DiseasePestKnowledgeRepository(base)
DiseasePestKnowledgeValidator().validate(repo)

print("Disease/Pest knowledge validation: PASS")
print(f"Diseases: {len(repo.diseases)}")
print(f"Pests: {len(repo.pests)}")
print(f"Symptoms: {len(repo.symptoms)}")
print(f"Disease progression records: {len(repo.disease_progression)}")
print(f"Disease condition records: {len(repo.disease_conditions)}")
print(f"Management records: {len(repo.management)}")
