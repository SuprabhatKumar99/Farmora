from .models import FarmDigitalProfile


class FarmDigitalProfileService:
    def __init__(self, repository):
        self.repository = repository

    def get_farm_profile(self, farm_id: str) -> FarmDigitalProfile:
        farm = self.repository.get_farm(farm_id)

        if farm is None:
            raise ValueError(f"Unknown farm_id: {farm_id}")

        return FarmDigitalProfile(
            farm=farm,
            fields=self.repository.get_fields(farm_id),
            zones=self.repository.get_zones(farm_id),
            crop_cycles=self.repository.get_crop_cycles(farm_id),
        )

    def get_zone_profile(self, zone_id: str) -> dict:
        zone = self.repository.get_zone(zone_id)

        if zone is None:
            raise ValueError(f"Unknown zone_id: {zone_id}")

        return {
            "zone": zone,
            "crop_cycles": self.repository.get_crop_cycles_for_zone(zone_id),
        }

    def get_active_crop_cycles(self, farm_id: str) -> list[dict]:
        return self.repository.get_crop_cycles(farm_id)
