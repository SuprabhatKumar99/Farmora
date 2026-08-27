from .models import CropContext

class CropKnowledgeService:
    def __init__(self, repository):
        self.repository = repository

    def get_crop_context(self, crop_id, variety_id=None):
        crop = self.repository.get_crop(crop_id)
        if crop is None:
            raise ValueError(f"Unknown crop_id: {crop_id}")

        if variety_id is not None:
            valid = {str(v["variety_id"]) for v in self.repository.get_varieties(crop_id)}
            if str(variety_id) not in valid:
                raise ValueError(f"variety_id {variety_id} does not belong to crop {crop_id}")

        return CropContext(
            crop=crop,
            varieties=self.repository.get_varieties(crop_id),
            growth_stages=self.repository.get_growth_stages(crop_id),
            crop_lifecycle=self.repository.get_crop_lifecycle(crop_id),
            requirements=self.repository.get_requirements(crop_id, variety_id),
        )
