import time
from ..preprocessing.tabular import EnvironmentPreprocessor
from ..schemas.models import EnvironmentWeatherResult,ModelTask
class Expert5EnvironmentWeatherService:
    def __init__(self,model=None): self.model=model; self.preprocessor=EnvironmentPreprocessor()
    def set_model(self,model): self.model=model
    def analyze(self,observation_id,data_path):
        t=time.perf_counter()
        if self.model is None: return self.err(observation_id,'MODEL_NOT_LOADED','Expert 5 model is not loaded.',t)
        try:
            df=self.preprocessor.load(data_path); self.preprocessor.validate_timestamp(df); raw=self.model.predict(df)
            preds=[] if raw is None else raw if isinstance(raw,list) else [raw]
            return EnvironmentWeatherResult(observation_id=observation_id,model_name=self.model.name,model_version=self.model.version,task=ModelTask(self.model.task),records_processed=len(df),predictions=preds,processing_time_ms=(time.perf_counter()-t)*1000,evidence_quality='ACCEPTABLE',status='COMPLETED')
        except FileNotFoundError as e: return self.err(observation_id,'DATA_NOT_FOUND',str(e),t)
        except Exception as e: return self.err(observation_id,'INFERENCE_FAILED',str(e),t)
    def err(self,oid,code,msg,t):
        return EnvironmentWeatherResult(observation_id=oid,model_name=getattr(self.model,'name','unknown'),model_version=getattr(self.model,'version','unknown'),task=ModelTask(getattr(self.model,'task','FORECASTING')),records_processed=0,processing_time_ms=(time.perf_counter()-t)*1000,evidence_quality='UNKNOWN',status='FAILED',error_code=code,error_message=msg)
