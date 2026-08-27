from pathlib import Path
import pandas as pd

class DiseasePestKnowledgeRepository:
    # Structure is preserved exactly.
    FILES = (
        "diseases.csv",
        "pests.csv",
        "symptoms.csv",
        "disease_progression.csv",
        "disease_conditions.csv",
        "management.csv",
    )

    def __init__(self, base_path: str | Path):
        self.base_path = Path(base_path)
        if not self.base_path.exists():
            raise FileNotFoundError(f"Knowledge directory not found: {self.base_path}")
        self.diseases = self._load("diseases.csv")
        self.pests = self._load("pests.csv")
        self.symptoms = self._load("symptoms.csv")
        self.disease_progression = self._load("disease_progression.csv")
        self.disease_conditions = self._load("disease_conditions.csv")
        self.management = self._load("management.csv")

    def _load(self, filename):
        path = self.base_path / filename
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")
        return pd.read_csv(path)

    @staticmethod
    def _filter(df, column, value):
        if column not in df.columns:
            return df.iloc[0:0]
        return df[df[column].astype(str) == str(value)]

    def get_disease(self, disease_id):
        r = self._filter(self.diseases, "disease_id", disease_id)
        return None if r.empty else r.iloc[0].to_dict()

    def get_diseases_for_crop(self, crop_id):
        return self._filter(self.diseases, "crop_id", crop_id).to_dict(orient="records")

    def get_pests_for_crop(self, crop_id):
        return self._filter(self.pests, "crop_id", crop_id).to_dict(orient="records")

    def get_symptoms_for_disease(self, disease_id):
        return self._filter(self.symptoms, "disease_id", disease_id).to_dict(orient="records")

    def get_progression_for_disease(self, disease_id):
        if "disease_id" not in self.disease_progression.columns:
            return self.disease_progression.to_dict(orient="records")
        return self._filter(self.disease_progression, "disease_id", disease_id).to_dict(orient="records")

    def get_conditions_for_disease(self, disease_id):
        if "disease_id" not in self.disease_conditions.columns:
            return self.disease_conditions.to_dict(orient="records")
        return self._filter(self.disease_conditions, "disease_id", disease_id).to_dict(orient="records")

    def get_management_for_disease(self, disease_id):
        if "disease_id" not in self.management.columns:
            return self.management.to_dict(orient="records")
        return self._filter(self.management, "disease_id", disease_id).to_dict(orient="records")

    def get_disease_context(self, disease_id):
        disease = self.get_disease(disease_id)
        if disease is None:
            raise ValueError(f"Unknown disease_id: {disease_id}")
        return {
            "disease": disease,
            "symptoms": self.get_symptoms_for_disease(disease_id),
            "progression": self.get_progression_for_disease(disease_id),
            "conditions": self.get_conditions_for_disease(disease_id),
            "management": self.get_management_for_disease(disease_id),
        }
