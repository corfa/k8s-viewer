from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_k8s_service
from services.base_k8s_service import BaseSerivceK8s
from api.schemas.response_deployments import DeploymentsResponse

router = APIRouter()


@router.get("/deployments")
async def get_deployments(namespace: str | None = None,
                          k8s_service: BaseSerivceK8s = Depends(get_k8s_service)
                          ) -> DeploymentsResponse:
    try:
        deployments = k8s_service.get_deployments(namespace)
        return DeploymentsResponse(results=deployments)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch deployments: {str(e)}"
        )
