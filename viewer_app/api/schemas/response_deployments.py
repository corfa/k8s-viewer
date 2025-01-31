from pydantic import BaseModel

from services.domain.deployments import DeploymentsSnapshot


class DeploymentsResponse(BaseModel):
    results: DeploymentsSnapshot
