from fastapi import FastAPI
from api.routers.k8s import router as k8s_router


app = FastAPI()
app.include_router(k8s_router)
