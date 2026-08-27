class InMemoryDiseaseEventStore:
    """Development persistence adapter.

    The production system can replace this with the backend persistence
    layer without changing the event/progression service contract.
    """

    def __init__(self):
        self.events = {}
        self.evidence = {}
        self.progression = {}

    def save_event(self, event):
        self.events[event.event_id] = event
        return event

    def get_event(self, event_id):
        return self.events.get(event_id)

    def save_evidence(self, evidence):
        self.evidence[evidence.evidence_id] = evidence
        return evidence

    def list_evidence(self, event_id):
        return [
            item
            for item in self.evidence.values()
            if item.event_id == event_id
        ]

    def save_progression(self, observation):
        self.progression[observation.observation_id] = observation
        return observation

    def list_progression(self, event_id):
        return sorted(
            [
                item
                for item in self.progression.values()
                if item.event_id == event_id
            ],
            key=lambda item: item.observed_at,
        )
