class DecisionInferenceEngine:
    """Actual Expert 8 inference execution."""

    def __init__(self, model):
        self.model = model

    def run(self, prompt: str) -> str:
        if self.model is None:
            raise RuntimeError("MODEL_NOT_LOADED")
        return self.model.predict(prompt)
