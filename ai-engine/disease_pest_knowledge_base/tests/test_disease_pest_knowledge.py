from pathlib import Path
from app.knowledge.repository import DiseasePestKnowledgeRepository
from app.knowledge.service import DiseasePestKnowledgeService
from app.knowledge.validator import DiseasePestKnowledgeValidator

BASE = Path("data/crop_health_dataset/02_disease_pest_knowledge")

def repo():
    r = DiseasePestKnowledgeRepository(BASE)
    DiseasePestKnowledgeValidator().validate(r)
    return r

def test_dataset_loads():
    r = repo()
    assert len(r.diseases) > 0
    assert len(r.pests) > 0
    assert len(r.symptoms) > 0
    assert len(r.disease_progression) > 0
    assert len(r.disease_conditions) > 0
    assert len(r.management) > 0

def test_disease_context():
    c = DiseasePestKnowledgeService(repo()).get_disease_context("D001")
    assert c["disease"]["disease_id"] == "D001"
    assert len(c["symptoms"]) == 1
    assert len(c["progression"]) == 1
    assert len(c["conditions"]) == 1
    assert len(c["management"]) == 1
