from fastapi import FastAPI
from app.experts.expert2_chemical_pesticide_damage.api.routes import router
app=FastAPI(title="Agricultural AI Engine — Expert 2")
app.include_router(router)
@app.get("/health")
def health(): return {"status":"UP","expert":"EXPERT_2_CHEMICAL_PESTICIDE_DAMAGE"}
@app.get("/ready")
def ready(): return {"status":"READY"}
