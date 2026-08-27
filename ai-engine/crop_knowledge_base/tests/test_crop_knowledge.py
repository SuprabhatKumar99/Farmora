from pathlib import Path
from app.knowledge.repository import CropKnowledgeRepository
from app.knowledge.service import CropKnowledgeService
from app.knowledge.validator import CropKnowledgeValidator

BASE = Path("data/crop_health_dataset/01_crop_knowledge")

def repo():
    r = CropKnowledgeRepository(BASE)
    CropKnowledgeValidator().validate(r)
    return r

def test_load():
    r = repo()
    assert len(r.crops) > 0
    assert len(r.varieties) > 0
    assert len(r.growth_stages) > 0
    assert len(r.crop_lifecycle) > 0
    assert len(r.crop_requirements) > 0

def test_context():
    c = CropKnowledgeService(repo()).get_crop_context("C001", "V001")
    assert c.crop["crop_id"] == "C001"
    assert len(c.growth_stages) == 5
    assert len(c.requirements) == 1

