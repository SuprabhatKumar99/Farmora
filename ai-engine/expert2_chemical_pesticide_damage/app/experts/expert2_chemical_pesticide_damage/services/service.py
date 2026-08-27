import time
from .preprocessing.image import ImagePreprocessor
from .schemas.models import BoundingBox,ChemicalDamageDetection,ChemicalDamageResult,ModelTask

class Expert2ChemicalDamageService:
    def __init__(self,model=None): self.model=model; self.preprocessor=ImagePreprocessor()
    def set_model(self,model): self.model=model
    def analyze(self,observation_id,image_path,confidence_threshold=.25):
        t=time.perf_counter()
        if self.model is None: return self._err(observation_id,"MODEL_NOT_LOADED","Expert 2 model is not loaded.",t)
        try:
            img=self.preprocessor.load(image_path); raw=self.model.predict(img,confidence_threshold)
            ds=[]
            for x in raw or []:
                b=x.get("bbox")
                ds.append(ChemicalDamageDetection(class_id=int(x["class_id"]),class_name=str(x["class_name"]),confidence=float(x["confidence"]),
                    bbox=BoundingBox(x1=b[0],y1=b[1],x2=b[2],y2=b[3]) if b else None))
            return ChemicalDamageResult(observation_id=observation_id,model_name=self.model.name,model_version=self.model.version,
                task=ModelTask(self.model.task),detections=ds,processing_time_ms=(time.perf_counter()-t)*1000,
                evidence_quality=self.preprocessor.quality(img),status="COMPLETED")
        except FileNotFoundError as e: return self._err(observation_id,"IMAGE_NOT_FOUND",str(e),t)
        except Exception as e: return self._err(observation_id,"INFERENCE_FAILED",str(e),t)
    def _err(self,oid,code,msg,t):
        return ChemicalDamageResult(observation_id=oid,model_name=getattr(self.model,"name","unknown"),
            model_version=getattr(self.model,"version","unknown"),task=ModelTask(getattr(self.model,"task","CLASSIFICATION")),
            processing_time_ms=(time.perf_counter()-t)*1000,evidence_quality="UNKNOWN",status="FAILED",
            error_code=code,error_message=msg)
