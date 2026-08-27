class FarmDigitalProfileValidator:
    REQUIRED_FARM_COLUMNS = {
        "farm_id",
        "location",
        "latitude",
        "longitude",
        "area_hectares",
        "soil_type",
    }

    REQUIRED_ZONE_COLUMNS = {
        "zone_id",
        "farm_id",
        "zone_number",
        "area_m2",
        "latitude",
        "longitude",
    }

    REQUIRED_CROP_CYCLE_COLUMNS = {
        "cycle_id",
        "farm_id",
        "zone_id",
        "crop_id",
        "variety_id",
        "sowing_date",
        "expected_harvest_date",
        "current_stage",
    }

    def validate(self, repository) -> None:
        self._check_columns(
            repository.farms,
            self.REQUIRED_FARM_COLUMNS,
            "farms.csv",
        )

        # fields.csv is part of the required project structure.
        # Its exact columns were not specified in the supplied dataset
        # document, so its records are loaded without inventing a schema.
        self._check_columns(
            repository.zones,
            self.REQUIRED_ZONE_COLUMNS,
            "zones.csv",
        )

        self._check_columns(
            repository.crop_cycles,
            self.REQUIRED_CROP_CYCLE_COLUMNS,
            "crop_cycles.csv",
        )

        self._check_unique(
            repository.farms,
            "farm_id",
            "farms.csv",
        )

        self._check_unique(
            repository.zones,
            "zone_id",
            "zones.csv",
        )

        self._check_unique(
            repository.crop_cycles,
            "cycle_id",
            "crop_cycles.csv",
        )

        self._check_fk(
            repository.zones,
            repository.farms,
            "farm_id",
            "farm_id",
            "zones.csv",
            "farms.csv",
        )

        self._check_fk(
            repository.crop_cycles,
            repository.farms,
            "farm_id",
            "farm_id",
            "crop_cycles.csv",
            "farms.csv",
        )

        self._check_fk(
            repository.crop_cycles,
            repository.zones,
            "zone_id",
            "zone_id",
            "crop_cycles.csv",
            "zones.csv",
        )

        self._check_zone_farm_consistency(repository)

    @staticmethod
    def _check_columns(df, required, filename):
        missing = required - set(df.columns)

        if missing:
            raise ValueError(
                f"{filename}: missing columns {sorted(missing)}"
            )

    @staticmethod
    def _check_unique(df, key, filename):
        duplicates = df[df[key].duplicated(keep=False)]

        if not duplicates.empty:
            values = sorted(
                duplicates[key]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            raise ValueError(
                f"{filename}: duplicate {key}: {values}"
            )

    @staticmethod
    def _check_fk(
        child,
        parent,
        child_key,
        parent_key,
        child_name,
        parent_name,
    ):
        child_values = set(
            child[child_key].dropna().astype(str)
        )

        parent_values = set(
            parent[parent_key].dropna().astype(str)
        )

        invalid = child_values - parent_values

        if invalid:
            raise ValueError(
                f"{child_name}: invalid {child_key} values "
                f"not present in {parent_name}: {sorted(invalid)}"
            )

    @staticmethod
    def _check_zone_farm_consistency(repository):
        farm_by_zone = {
            str(row.zone_id): str(row.farm_id)
            for row in repository.zones.itertuples()
        }

        mismatches = []

        for row in repository.crop_cycles.itertuples():
            zone_id = str(row.zone_id)
            farm_id = str(row.farm_id)

            if zone_id in farm_by_zone:
                if farm_by_zone[zone_id] != farm_id:
                    mismatches.append(
                        (str(row.cycle_id), farm_id, zone_id, farm_by_zone[zone_id])
                    )

        if mismatches:
            raise ValueError(
                "crop_cycles.csv: farm_id does not match the farm_id "
                f"of its zone: {mismatches}"
            )
