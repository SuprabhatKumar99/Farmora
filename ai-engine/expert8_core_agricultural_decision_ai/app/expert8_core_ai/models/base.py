from abc import ABC, abstractmethod


class AgriculturalDecisionModel(ABC):
    name = "unknown"
    version = "unknown"

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def predict(self, structured_context: dict):
        raise NotImplementedError

    def metadata(self):
        return {
            "name": self.name,
            "version": self.version,
        }
