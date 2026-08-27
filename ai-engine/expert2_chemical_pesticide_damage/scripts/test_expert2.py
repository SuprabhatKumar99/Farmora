import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.experts.expert2_chemical_pesticide_damage.api.routes import get_service
from app.experts.expert2_chemical_pesticide_damage.models.loader import ChemicalDamageModelLoader
if len(sys.argv)!=3: raise SystemExit("Usage: python scripts/test_expert2.py <model.pt> <image>")
s=get_service(); s.set_model(ChemicalDamageModelLoader().load_torchscript(sys.argv[1],task="DETECTION"))
print(s.analyze("LOCAL-TEST",sys.argv[2]).model_dump(mode="json"))
