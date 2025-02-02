from pydantic import BaseModel


class ResponseDeployments(BaseModel):
    results: dict
