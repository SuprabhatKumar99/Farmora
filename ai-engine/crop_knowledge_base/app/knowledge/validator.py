class CropKnowledgeValidator:
    REQUIRED_CROP_COLUMNS = {"crop_id","crop_name","scientific_name","family","lifecycle"}
    REQUIRED_VARIETY_COLUMNS = {"variety_id","crop_id","variety_name","maturity_days","disease_susceptibility"}
    REQUIRED_GROWTH_STAGE_COLUMNS = {"stage_id","crop_id","stage_name","start_day","end_day","expected_features"}
    REQUIRED_REQUIREMENT_COLUMNS = {
        "crop_id","variety_id","temperature_min","temperature_max",
        "humidity_min","humidity_max","soil_moisture_min","soil_moisture_max"
    }

    def validate(self, repository):
        self._columns(repository.crops, self.REQUIRED_CROP_COLUMNS, "crops.csv")
        self._columns(repository.varieties, self.REQUIRED_VARIETY_COLUMNS, "varieties.csv")
        self._columns(repository.growth_stages, self.REQUIRED_GROWTH_STAGE_COLUMNS, "growth_stages.csv")
        self._columns(repository.crop_requirements, self.REQUIRED_REQUIREMENT_COLUMNS, "crop_requirements.csv")

        self._unique(repository.crops, "crop_id", "crops.csv")
        self._unique(repository.varieties, "variety_id", "varieties.csv")
        self._unique(repository.growth_stages, "stage_id", "growth_stages.csv")

        self._fk(repository.varieties, repository.crops, "crop_id", "crop_id", "varieties.csv", "crops.csv")
        self._fk(repository.growth_stages, repository.crops, "crop_id", "crop_id", "growth_stages.csv", "crops.csv")
        self._fk(repository.crop_requirements, repository.crops, "crop_id", "crop_id", "crop_requirements.csv", "crops.csv")

        if "variety_id" in repository.crop_requirements.columns:
            self._fk(repository.crop_requirements, repository.varieties, "variety_id", "variety_id",
                     "crop_requirements.csv", "varieties.csv", allow_null=True)

        invalid = repository.growth_stages[
            repository.growth_stages["start_day"].notna()
            & repository.growth_stages["end_day"].notna()
            & (repository.growth_stages["start_day"] > repository.growth_stages["end_day"])
        ]
        if not invalid.empty:
            raise ValueError("growth_stages.csv: start_day cannot be greater than end_day")

    @staticmethod
    def _columns(df, required, filename):
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{filename}: missing columns {sorted(missing)}")

    @staticmethod
    def _unique(df, key, filename):
        dup = df[df[key].duplicated(keep=False)]
        if not dup.empty:
            raise ValueError(f"{filename}: duplicate {key}: {sorted(dup[key].dropna().astype(str).unique())}")

    @staticmethod
    def _fk(child, parent, child_key, parent_key, child_name, parent_name, allow_null=False):
        values = child[child_key].dropna() if allow_null else child[child_key]
        invalid = set(values.astype(str)) - set(parent[parent_key].dropna().astype(str))
        if invalid:
            raise ValueError(f"{child_name}: invalid {child_key}: {sorted(invalid)}")
