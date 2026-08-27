from .models import DiseasePestContext

class DiseasePestKnowledgeService:
    def __init__(self, repository):
        self.repository = repository

    def get_disease_context(self, disease_id):
        return self.repository.get_disease_context(disease_id)

    def get_crop_context(self, crop_id):
        return DiseasePestContext(
            diseases=self.repository.get_diseases_for_crop(crop_id),
            pests=self.repository.get_pests_for_crop(crop_id),
            symptoms=[],
            disease_progression=[],
            disease_conditions=[],
            management=[],
        )

    def get_symptoms(self, disease_id):
        return self.repository.get_symptoms_for_disease(disease_id)

    def get_progression(self, disease_id):
        return self.repository.get_progression_for_disease(disease_id)

    def get_conditions(self, disease_id):
        return self.repository.get_conditions_for_disease(disease_id)

    def get_management(self, disease_id):
        return self.repository.get_management_for_disease(disease_id)
