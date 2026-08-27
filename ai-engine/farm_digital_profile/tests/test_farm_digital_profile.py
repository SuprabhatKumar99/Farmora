from pathlib import Path

from app.knowledge.repository import FarmDigitalProfileRepository
from app.knowledge.service import FarmDigitalProfileService
from app.knowledge.validator import FarmDigitalProfileValidator


BASE = Path("data/crop_health_dataset/03_farm")


def repository():
    repo = FarmDigitalProfileRepository(BASE)
    FarmDigitalProfileValidator().validate(repo)
    return repo


def test_dataset_loads():
    repo = repository()

    assert len(repo.farms) > 0
    assert len(repo.fields) > 0
    assert len(repo.zones) > 0
    assert len(repo.crop_cycles) > 0


def test_farm_lookup():
    farm = repository().get_farm("F001")

    assert farm is not None
    assert farm["farm_id"] == "F001"


def test_zone_lookup():
    zone = repository().get_zone("Z001")

    assert zone is not None
    assert zone["farm_id"] == "F001"


def test_crop_cycle_lookup():
    cycles = repository().get_crop_cycles("F001")

    assert len(cycles) == 2
    assert cycles[0]["farm_id"] == "F001"


def test_complete_farm_profile():
    service = FarmDigitalProfileService(repository())

    profile = service.get_farm_profile("F001")

    assert profile.farm["farm_id"] == "F001"
    assert len(profile.zones) == 2
    assert len(profile.crop_cycles) == 2


def test_zone_profile():
    service = FarmDigitalProfileService(repository())

    profile = service.get_zone_profile("Z001")

    assert profile["zone"]["zone_id"] == "Z001"
    assert len(profile["crop_cycles"]) == 1


def test_invalid_farm():
    service = FarmDigitalProfileService(repository())

    try:
        service.get_farm_profile("INVALID")
    except ValueError:
        return

    raise AssertionError("Expected ValueError")
