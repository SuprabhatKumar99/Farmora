from pathlib import Path
import cv2,numpy as np
from app.experts.expert2_chemical_pesticide_damage.services.service import Expert2ChemicalDamageService
class Fake:
    name="fake-expert2"; version="test-1"; task="DETECTION"
    def predict(self,image,confidence_threshold):
        return [{"class_id":1,"class_name":"chemical_damage_pattern","confidence":.91,"bbox":[2,3,20,21]}]
def test_service(tmp_path):
    p=tmp_path/"x.jpg"; cv2.imwrite(str(p),np.zeros((64,64,3),dtype=np.uint8))
    r=Expert2ChemicalDamageService(Fake()).analyze("OBS-1",str(p))
    assert r.status=="COMPLETED" and len(r.detections)==1
def test_missing_model(tmp_path):
    p=tmp_path/"x.jpg"; cv2.imwrite(str(p),np.zeros((64,64,3),dtype=np.uint8))
    r=Expert2ChemicalDamageService().analyze("OBS-1",str(p))
    assert r.error_code=="MODEL_NOT_LOADED"
