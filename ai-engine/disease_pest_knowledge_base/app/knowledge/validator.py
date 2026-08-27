class DiseasePestKnowledgeValidator:
    REQUIRED_DISEASE_COLUMNS = {
        "disease_id","disease_name","crop_id","pathogen_type",
        "pathogen_name","affected_parts","typical_stage"
    }
    REQUIRED_PEST_COLUMNS = {
        "pest_id","pest_name","crop_id","affected_parts","typical_stage"
    }
    REQUIRED_SYMPTOM_COLUMNS = {
        "symptom_id","disease_id","crop_id","plant_part","symptom_type",
        "color","pattern","severity_stage","description"
    }

    def validate(self, repo):
        self._columns(repo.diseases, self.REQUIRED_DISEASE_COLUMNS, "diseases.csv")
        self._columns(repo.pests, self.REQUIRED_PEST_COLUMNS, "pests.csv")
        self._columns(repo.symptoms, self.REQUIRED_SYMPTOM_COLUMNS, "symptoms.csv")

        self._unique(repo.diseases, "disease_id", "diseases.csv")
        self._unique(repo.pests, "pest_id", "pests.csv")
        self._unique(repo.symptoms, "symptom_id", "symptoms.csv")

        self._fk(repo.symptoms, repo.diseases, "disease_id", "disease_id",
                 "symptoms.csv", "diseases.csv")

        disease_crop = {
            str(r.disease_id): str(r.crop_id)
            for r in repo.diseases.itertuples()
        }
        for r in repo.symptoms.itertuples():
            did = str(r.disease_id)
            if did in disease_crop and disease_crop[did] != str(r.crop_id):
                raise ValueError(
                    f"symptoms.csv: crop_id mismatch for disease_id={did}"
                )

    @staticmethod
    def _columns(df, required, filename):
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{filename}: missing columns {sorted(missing)}")

    @staticmethod
    def _unique(df, key, filename):
        dup = df[df[key].duplicated(keep=False)]
        if not dup.empty:
            raise ValueError(f"{filename}: duplicate {key}")

    @staticmethod
    def _fk(child, parent, child_key, parent_key, child_name, parent_name):
        invalid = (
            set(child[child_key].dropna().astype(str))
            - set(parent[parent_key].dropna().astype(str))
        )
        if invalid:
            raise ValueError(
                f"{child_name}: invalid {child_key} values not present in "
                f"{parent_name}: {sorted(invalid)}"
            )
