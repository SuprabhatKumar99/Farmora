from app.validation_ground_truth.schemas.models import GroundTruthRecord


class GroundTruthStore:
    """In-memory reference implementation.

    Production persistence belongs to the backend/database layer. This store
    exists so Step 18 can be tested without inventing a database dependency.
    """

    def __init__(self):
        self._records = {}

    def add(self, record: GroundTruthRecord):
        if record.case_id in self._records:
            raise ValueError("GROUND_TRUTH_ALREADY_EXISTS")
        self._records[record.case_id] = record

    def get(self, case_id: str) -> GroundTruthRecord | None:
        return self._records.get(case_id)

    def list(self):
        return list(self._records.values())
