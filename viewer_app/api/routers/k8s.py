from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_service_deployment
from api.schemas.response_deployments import ResponseDeployments
router = APIRouter()


@router.get("/deployments")
async def get_deployments(
    namespace: str | None = None,
    deployment_service=Depends(get_service_deployment)
) -> ResponseDeployments:
    try:
        deployments = await deployment_service.get_deployments(namespace)
        return ResponseDeployments(results=deployments.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch deployments: {str(e)}"
        )
