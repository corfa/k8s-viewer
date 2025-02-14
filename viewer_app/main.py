from fastapi import FastAPI

from api.routers.k8s import router as k8s_router
from core.db import database

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(k8s_router)
