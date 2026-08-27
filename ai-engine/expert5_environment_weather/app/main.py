from fastapi import FastAPI
from app.experts.expert5_environment_weather.api.routes import router
app=FastAPI(title='Agricultural AI Engine — Expert 5'); app.include_router(router)
@app.get('/health')
def health(): return {'status':'UP','expert':'EXPERT_5_ENVIRONMENT_WEATHER'}
@app.get('/ready')
def ready(): return {'status':'READY'}
