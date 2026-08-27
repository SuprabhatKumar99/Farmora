from datetime import datetime, timezone
from uuid import uuid4

from app.followup_feedback.events.event_types import FeedbackEventType


def build_event(event_type: FeedbackEventType, case_id: str, payload: dict):
    return {
        "event_id": str(uuid4()),
        "event_type": event_type.value,
        "case_id": case_id,
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
