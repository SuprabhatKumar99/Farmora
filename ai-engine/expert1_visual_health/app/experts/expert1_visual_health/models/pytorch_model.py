from pathlib import Path
import torch
from .base import VisualHealthModel

class TorchScriptVisualModel(VisualHealthModel):
    """Adapter for a user-supplied TorchScript model.

    The exact tensor preprocessing/output decoding is intentionally not
    invented. It must match the supplied model's documented contract.
    """

    def __init__(self, model_path, name="user_provided_visual_health_model",
                 version="provided", task="CLASSIFICATION", device=None):
        self.model_path = Path(model_path)
        self.name = name
        self.version = version
        self.task = task
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"Trained model not found: {self.model_path}")
        self.model = torch.jit.load(str(self.model_path), map_location=self.device)
        self.model.eval()

    def predict(self, image, confidence_threshold: float):
        if self.model is None:
            raise RuntimeError("Model is not loaded.")
        raise NotImplementedError(
            "Implement preprocessing/output decoding for the supplied model."
        )
