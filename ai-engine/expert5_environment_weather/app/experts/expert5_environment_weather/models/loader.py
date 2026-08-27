from .pytorch_model import TorchScriptEnvironmentWeatherModel
class EnvironmentWeatherModelLoader:
    def load_torchscript(self,model_path,name='user_provided_environment_weather_model',version='provided',task='FORECASTING',device=None):
        m=TorchScriptEnvironmentWeatherModel(model_path,name,version,task,device); m.load(); return m
