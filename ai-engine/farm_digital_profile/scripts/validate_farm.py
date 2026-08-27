import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.knowledge.repository import FarmDigitalProfileRepository
from app.knowledge.validator import FarmDigitalProfileValidator


base = (
    Path(__file__).resolve().parents[1]
    / "data/crop_health_dataset/03_farm"
)

repository = FarmDigitalProfileRepository(base)
FarmDigitalProfileValidator().validate(repository)

print("Farm Digital Profile validation: PASS")
print(f"Farms: {len(repository.farms)}")
print(f"Fields: {len(repository.fields)}")
print(f"Zones: {len(repository.zones)}")
print(f"Crop cycles: {len(repository.crop_cycles)}")
