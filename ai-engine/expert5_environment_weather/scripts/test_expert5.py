import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.experts.expert5_environment_weather.api.routes import get_service
from app.experts.expert5_environment_weather.models.loader import EnvironmentWeatherModelLoader
if len(sys.argv)!=3: raise SystemExit('Usage: python scripts/test_expert5.py <torchscript-model> <data.csv>')
s=get_service(); s.set_model(EnvironmentWeatherModelLoader().load_torchscript(sys.argv[1],task='FORECASTING')); print(s.analyze('LOCAL-TEST',sys.argv[2]).model_dump(mode='json'))
