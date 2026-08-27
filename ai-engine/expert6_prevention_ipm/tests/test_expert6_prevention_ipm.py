from pathlib import Path

import pandas as pd

from app.experts.expert6_prevention_ipm.preprocessing.input import (
    PreventionIPMPreprocessor,
)
from app.experts.expert6_prevention_ipm.services.service import (
    Expert6PreventionIPMService,
)


class FakePreventionIPMModel:
    name = "fake-expert6"
    version = "test-1"
    task = "RECOMMENDATION"

    def predict(self, dataframe):
        return [
            {
                "action_id": "A-TEST",
                "action_type": "TEST_ACTION",
                "priority": 0.8,
                "evidence_ids": ["E-TEST"],
            }
        ]


def create_data(path: Path):
    pd.DataFrame(
        {
            "case_id": ["CASE-001"],
            "observed_problem": ["example"],
        }
    ).to_csv(path, index=False)


def test_preprocessor_loads_input(tmp_path):
    path = tmp_path / "case.csv"
    create_data(path)

    dataframe = PreventionIPMPreprocessor().load(path)

    assert len(dataframe) == 1


def test_expert6_service_with_test_model(tmp_path):
    path = tmp_path / "case.csv"
    create_data(path)

    service = Expert6PreventionIPMService(
        model=FakePreventionIPMModel()
    )

    result = service.analyze(
        case_id="CASE-001",
        input_path=str(path),
    )

    assert result.status == "COMPLETED"
    assert result.expert == "EXPERT_6_PREVENTION_IPM"
    assert result.model_version == "test-1"
    assert len(result.actions) == 1


def test_missing_model_is_reported(tmp_path):
    path = tmp_path / "case.csv"
    create_data(path)

    service = Expert6PreventionIPMService()

    result = service.analyze(
        case_id="CASE-001",
        input_path=str(path),
    )

    assert result.status == "FAILED"
    assert result.error_code == "MODEL_NOT_LOADED"
