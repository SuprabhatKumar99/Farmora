from datetime import datetime, timezone
from uuid import uuid4

from app.disease_events.processing.progression import DiseaseProgressionEngine
from app.disease_events.processing.validation import DiseaseEventValidator
from app.disease_events.schemas.models import (
    DiseaseEvent,
    DiseaseEventEvidence,
    DiseaseEventTimeline,
    EvidenceType,
    ProgressionObservation,
)


class DiseaseEventService:
    def __init__(self, store, progression_engine=None, validator=None):
        self.store = store
        self.progression_engine = progression_engine or DiseaseProgressionEngine()
        self.validator = validator or DiseaseEventValidator()

    def create_event(
        self,
        farm_id: str,
        zone_id: str,
        first_observed_at: datetime,
        crop_id: str | None = None,
        variety_id: str | None = None,
        disease_id: str | None = None,
        pest_id: str | None = None,
        status="OBSERVED",
        severity: float | None = None,
    ):
        now = datetime.now(timezone.utc)

        event = DiseaseEvent(
            event_id=f"EVT-{uuid4().hex[:12]}",
            farm_id=farm_id,
            zone_id=zone_id,
            crop_id=crop_id,
            variety_id=variety_id,
            disease_id=disease_id,
            pest_id=pest_id,
            status=status,
            severity=severity,
            first_observed_at=first_observed_at,
            last_observed_at=first_observed_at,
            created_at=now,
            updated_at=now,
        )

        self.validator.validate_event(event)
        return self.store.save_event(event)

    def get_event(self, event_id):
        event = self.store.get_event(event_id)

        if event is None:
            raise KeyError(event_id)

        return event

    def add_evidence(
        self,
        event_id: str,
        evidence_type: EvidenceType,
        reference_id: str,
        observed_at: datetime,
        confidence: float | None = None,
        notes: str | None = None,
    ):
        event = self.get_event(event_id)

        evidence = DiseaseEventEvidence(
            evidence_id=f"EVD-{uuid4().hex[:12]}",
            event_id=event_id,
            evidence_type=evidence_type,
            reference_id=reference_id,
            observed_at=observed_at,
            confidence=confidence,
            notes=notes,
        )

        self.validator.validate_evidence(event, evidence)
        return self.store.save_evidence(evidence)

    def add_progression_observation(
        self,
        event_id: str,
        observed_at: datetime,
        severity: float,
        evidence_ids=None,
    ):
        event = self.get_event(event_id)

        observation = ProgressionObservation(
            observation_id=f"PROG-{uuid4().hex[:12]}",
            event_id=event_id,
            observed_at=observed_at,
            severity=severity,
            evidence_ids=evidence_ids or [],
        )

        self.validator.validate_progression(event, observation)
        return self.store.save_progression(observation)

    def analyze_progression(self, event_id):
        event = self.get_event(event_id)
        observations = self.store.list_progression(event_id)

        return self.progression_engine.analyze(
            event_id=event_id,
            observations=observations,
        )

    def get_timeline(self, event_id):
        event = self.get_event(event_id)

        return DiseaseEventTimeline(
            event=event,
            evidence=self.store.list_evidence(event_id),
            progression=self.store.list_progression(event_id),
        )
