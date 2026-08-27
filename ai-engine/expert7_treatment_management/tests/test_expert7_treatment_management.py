from pathlib import Path

import pandas as pd

from app.experts.expert7_treatment_management.preprocessing.input import (
    TreatmentManagementPreprocessor,
)
from app.experts.expert7_treatment_management.services.service import (
    Expert7TreatmentManagementService,
)


class FakeTreatmentModel:
    name = "fake-expert7"
    version = "test-1"
    task = "RECOMMENDATION"

    def predict(self, dataframe):
        return [
            {
                "treatment_id": "T-TEST",
                "treatment_type": "TEST_ACTION",
                "priority": 0.8,
                "evidence_ids": ["E-TEST"],
                "validation_required": True,
            }
        ]


def create_data(path: Path):
    pd.DataFrame(
        {
            "case_id": ["CASE-001"],
            "diagnosis_status": ["UNKNOWN"],
        }
    ).to_csv(path, index=False)


def test_preprocessor_loads_input(tmp_path):
    path = tmp_path / "case.csv"
    create_data(path)

    dataframe = TreatmentManagementPreprocessor().load(path)

    assert len(dataframe) == 1


def test_expert7_service_with_test_model(tmp_path):
    path = tmp_path / "case.csv"
    create_data(path)

    service = Expert7TreatmentManagementService(
        model=FakeTreatmentModel()
    )
    service.set_model(FakeTreatmentModel())

    result = service.analyze(
        case_id="CASE-001",
        input_path=str(path),
    )

    assert result.status == "COMPLETED"
    assert result.expert == "EXPERT_7_TREATMENT_MANAGEMENT"
    assert result.model_version == "test-1"
    assert len(result.treatments) == 1
    assert result.treatments[0].validation_required is True


def test_missing_model_is_reported(tmp_path):
    path = tmp_path / "case.csv"
    create_data(path)

    service = Expert7TreatmentManagementService()

    result = service.analyze(
        case_id="CASE-001",
        input_path=str(path),
    )

    assert result.status == "FAILED"
    assert result.error_code == "MODEL_NOT_LOADED"
