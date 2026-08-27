from abc import ABC,abstractmethod
class EnvironmentWeatherModel(ABC):
    name='unknown'; version='unknown'; task='FORECASTING'
    @abstractmethod
    def load(self): ...
    @abstractmethod
    def predict(self,dataframe): ...
    def metadata(self): return {'name':self.name,'version':self.version,'task':self.task}
