from abc import ABC, abstractmethod


class TreatmentManagementModel(ABC):
    """Stable interface for a supplied Expert 7 model."""

    name = "unknown"
    version = "unknown"
    task = "RECOMMENDATION"

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def predict(self, dataframe):
        raise NotImplementedError

    def metadata(self):
        return {
            "name": self.name,
            "version": self.version,
            "task": self.task,
        }
