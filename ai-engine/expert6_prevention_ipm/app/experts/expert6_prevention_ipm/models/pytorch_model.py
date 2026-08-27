from pathlib import Path
import torch

from .base import PreventionIPMModel


class TorchScriptPreventionIPMModel(PreventionIPMModel):
    """Adapter for a user-supplied TorchScript Expert 6 model.

    The model's real feature schema, encoding, output format, and action labels
    must be supplied. No IPM recommendation logic is fabricated here.
    """

    def __init__(
        self,
        model_path: str,
        name: str = "user_provided_prevention_ipm_model",
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
            "according to the supplied Expert 6 model contract."
        )
