import pandas as pd
from app.experts.expert5_environment_weather.services.service import Expert5EnvironmentWeatherService
class Fake:
    name='fake-expert5'; version='test-1'; task='FORECASTING'
    def predict(self,df): return [{'target':'test_prediction','value':0.5}]
def test_service(tmp_path):
    p=tmp_path/'x.csv'; pd.DataFrame({'timestamp':['2026-01-01T00:00:00'],'temperature_c':[25.0]}).to_csv(p,index=False)
    r=Expert5EnvironmentWeatherService(Fake()).analyze('OBS-1',str(p)); assert r.status=='COMPLETED' and len(r.predictions)==1
def test_no_model(tmp_path):
    p=tmp_path/'x.csv'; pd.DataFrame({'timestamp':['2026-01-01T00:00:00']}).to_csv(p,index=False)
    assert Expert5EnvironmentWeatherService().analyze('OBS-1',str(p)).error_code=='MODEL_NOT_LOADED'
