from .pytorch_model import TorchScriptChemicalDamageModel
class ChemicalDamageModelLoader:
    def load_torchscript(self,path,name="user_provided_chemical_damage_model",version="provided",task="CLASSIFICATION",device=None):
        m=TorchScriptChemicalDamageModel(path,name,version,task,device); m.load(); return m
