from abc import ABC, abstractmethod


class WholeCropHealthModel(ABC):
    """Stable model interface for the user-supplied Expert 4 model."""

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
        return {
            "name": self.name,
            "version": self.version,
            "task": self.task,
        }
