from pathlib import Path
import torch
from .base import ChemicalDamageModel
class TorchScriptChemicalDamageModel(ChemicalDamageModel):
    def __init__(self,path,name="user_provided_chemical_damage_model",version="provided",task="CLASSIFICATION",device=None):
        self.model_path=Path(path); self.name=name; self.version=version; self.task=task
        self.device=device or ("cuda" if torch.cuda.is_available() else "cpu"); self.model=None
    def load(self):
        if not self.model_path.exists(): raise FileNotFoundError(str(self.model_path))
        self.model=torch.jit.load(str(self.model_path),map_location=self.device); self.model.eval()
    def predict(self,image,confidence_threshold):
        if self.model is None: raise RuntimeError("Model is not loaded.")
        raise NotImplementedError("Implement model-specific preprocessing/output decoding from the supplied model contract.")
