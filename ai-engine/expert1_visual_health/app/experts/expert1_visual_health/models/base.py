from abc import ABC, abstractmethod

class VisualHealthModel(ABC):
    name = "unknown"
    version = "unknown"
    task = "CLASSIFICATION"

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def predict(self, image, confidence_threshold: float):
        raise NotImplementedError

    def metadata(self):
        return {"name": self.name, "version": self.version, "task": self.task}
