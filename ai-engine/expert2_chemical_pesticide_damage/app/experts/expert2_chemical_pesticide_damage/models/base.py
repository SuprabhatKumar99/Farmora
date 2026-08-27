from abc import ABC,abstractmethod
class ChemicalDamageModel(ABC):
    name="unknown"; version="unknown"; task="CLASSIFICATION"
    @abstractmethod
    def load(self): ...
    @abstractmethod
    def predict(self,image,confidence_threshold): ...
    def metadata(self): return {"name":self.name,"version":self.version,"task":self.task}
