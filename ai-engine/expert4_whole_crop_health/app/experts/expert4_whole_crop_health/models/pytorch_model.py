from pathlib import Path
import torch

from .base import WholeCropHealthModel


class TorchScriptWholeCropHealthModel(WholeCropHealthModel):
    """Adapter for a user-supplied TorchScript Expert 4 model.

    The concrete preprocessing and output decoding must match the supplied
    model contract. No class labels or architecture are fabricated.
    """

    def __init__(
        self,
        model_path: str,
        name: str = "user_provided_whole_crop_health_model",
        version: str = "provided",
        task: str = "CLASSIFICATION",
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

    def predict(self, image, confidence_threshold: float):
        if self.model is None:
            raise RuntimeError("Model is not loaded.")

        raise NotImplementedError(
            "Implement model-specific preprocessing and output decoding "
            "according to the supplied Expert 4 model contract."
        )
