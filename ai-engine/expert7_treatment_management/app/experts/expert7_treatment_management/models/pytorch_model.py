from pathlib import Path
import torch

from .base import TreatmentManagementModel


class TorchScriptTreatmentManagementModel(TreatmentManagementModel):
    """Adapter for a user-supplied TorchScript Expert 7 model.

    The real feature schema, output representation, treatment identifiers,
    ranking semantics, and validation requirements must come from the supplied
    model/data contract.
    """

    def __init__(
        self,
        model_path: str,
        name: str = "user_provided_treatment_management_model",
        version: str = "provided",
        task: str = "RECOMMENDATION",
        device: str | None = None,
    ):
        self.model_path = Path(model_path)
        self.name = name
        self.version = version
        self.task = task
        self.device = device or (
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.model = None

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Trained model not found: {self.model_path}"
            )

        self.model = torch.jit.load(
            str(self.model_path),
            map_location=self.device,
        )
        self.model.eval()

    def predict(self, dataframe):
        if self.model is None:
            raise RuntimeError("Model is not loaded.")

        raise NotImplementedError(
            "Implement model-specific feature preparation and output decoding "
            "according to the supplied Expert 7 model contract."
        )
