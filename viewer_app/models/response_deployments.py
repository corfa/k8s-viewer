from pydantic import BaseModel

from schemes.deployment import Deployment


class DeploymentsResponse(BaseModel):
    namespace: str
    deployments: list[Deployment]
