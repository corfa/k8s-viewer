from pydantic import BaseModel
from datetime import datetime


class Deployment(BaseModel):
    image: str
    envs: list[dict]


class DeploymentsSnapshot(BaseModel):
    deployments: list[Deployment]
    namespaces: str = "all-namespaces"
    count: int = 0
    time_response: datetime = datetime.now()
