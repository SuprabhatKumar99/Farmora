class TreatmentManagementInferenceEngine:
    """Executes the loaded Expert 7 model.

    Model loading remains in models/. This module owns actual inference
    execution so every expert follows the same architecture.
    """

    def __init__(self, model):
        self.model = model

    def run(self, prepared_input):
        if self.model is None:
            raise RuntimeError("MODEL_NOT_LOADED")

        return self.model.predict(prepared_input)
