from datetime import datetime, timedelta, timezone

from app.disease_events.processing.progression import DiseaseProgressionEngine
from app.disease_events.schemas.models import (
    EvidenceType,
    ProgressionObservation,
)
from app.disease_events.services.service import DiseaseEventService
from app.disease_events.storage.in_memory import InMemoryDiseaseEventStore


def make_service():
    return DiseaseEventService(InMemoryDiseaseEventStore())


def test_create_event():
    service = make_service()
    now = datetime.now(timezone.utc)

    event = service.create_event(
        farm_id="F001",
        zone_id="Z001",
        first_observed_at=now,
        crop_id="C001",
        disease_id="D001",
        severity=0.2,
    )

    assert event.event_id.startswith("EVT-")
    assert event.farm_id == "F001"


def test_add_evidence():
    service = make_service()
    now = datetime.now(timezone.utc)

    event = service.create_event(
        farm_id="F001",
        zone_id="Z001",
        first_observed_at=now,
    )

    evidence = service.add_evidence(
        event_id=event.event_id,
        evidence_type=EvidenceType.IMAGE,
        reference_id="OBS-001",
        observed_at=now,
        confidence=0.9,
    )

    assert evidence.event_id == event.event_id


def test_progression_increasing():
    service = make_service()
    start = datetime.now(timezone.utc)

    event = service.create_event(
        farm_id="F001",
        zone_id="Z001",
        first_observed_at=start,
    )

    # Extend the event observation window before adding the later observation.
    event.last_observed_at = start + timedelta(hours=24)
    service.store.save_event(event)

    service.add_progression_observation(
        event.event_id,
        start,
        0.2,
    )

    service.add_progression_observation(
        event.event_id,
        start + timedelta(hours=24),
        0.5,
    )

    result = service.analyze_progression(event.event_id)

    assert result.direction == "INCREASING"
    assert result.severity_change == 0.3
    assert result.elapsed_hours == 24.0


def test_single_progression_observation():
    start = datetime.now(timezone.utc)

    observation = ProgressionObservation(
        observation_id="P1",
        event_id="E1",
        observed_at=start,
        severity=0.4,
    )

    result = DiseaseProgressionEngine().analyze(
        "E1",
        [observation],
    )

    assert result.direction == "INSUFFICIENT_HISTORY"
    assert result.previous_severity is None


def test_progression_decreasing():
    start = datetime.now(timezone.utc)

    observations = [
        ProgressionObservation(
            observation_id="P1",
            event_id="E1",
            observed_at=start,
            severity=0.8,
        ),
        ProgressionObservation(
            observation_id="P2",
            event_id="E1",
            observed_at=start + timedelta(hours=12),
            severity=0.4,
        ),
    ]

    result = DiseaseProgressionEngine().analyze("E1", observations)

    assert result.direction == "DECREASING"
    assert result.severity_change == -0.4
    assert result.elapsed_hours == 12.0


def test_progression_stable():
    start = datetime.now(timezone.utc)

    observations = [
        ProgressionObservation(
            observation_id="P1",
            event_id="E1",
            observed_at=start,
            severity=0.4,
        ),
        ProgressionObservation(
            observation_id="P2",
            event_id="E1",
            observed_at=start + timedelta(hours=12),
            severity=0.4,
        ),
    ]

    result = DiseaseProgressionEngine().analyze("E1", observations)

    assert result.direction == "STABLE"
    assert result.severity_change == 0.0
