class TreatmentManagementPostprocessor:
    """Apply structural post-processing only.

    No agricultural treatment rule is introduced here.
    """

    def process(self, candidates):
        return sorted(
            candidates,
            key=lambda item: item["priority"],
            reverse=True,
        )
