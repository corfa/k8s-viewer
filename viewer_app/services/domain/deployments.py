from pydantic import BaseModel
from datetime import datetime


class Deployment(BaseModel):
    id: int = None
    image: str
    envs: list[dict] = []


class DeploymentsSnapshotCluster(BaseModel):
    deployments: list[Deployment]
    namespaces: str = "all-namespaces"
    count: int = 0
    time_response: datetime = datetime.now()
