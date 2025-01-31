from pydantic import BaseModel
from datetime import datetime

from clients.schemas.deployment import Deployment


class DeploymentsSnapshot(BaseModel):
    namespaces: str = "all-namespaces"
    count: int
    time_response: datetime = datetime.now()
    deployments: list[Deployment]
