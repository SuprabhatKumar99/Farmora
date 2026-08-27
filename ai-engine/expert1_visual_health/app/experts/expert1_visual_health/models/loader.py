from pathlib import Path
from .pytorch_model import TorchScriptVisualModel

class VisualModelLoader:
    def load_torchscript(self, model_path: str | Path,
                         name="user_provided_visual_health_model",
                         version="provided", task="CLASSIFICATION",
                         device=None):
        model = TorchScriptVisualModel(
            model_path, name=name, version=version,
            task=task, device=device
        )
        model.load()
        return model
