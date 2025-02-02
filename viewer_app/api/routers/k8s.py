from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_k8s_service
from services.k8s_service import K8sSerivce
from api.schemas.response_deployments import ResponseDeployments

router = APIRouter()


@router.get("/deployments")
async def get_deployments(namespace: str | None = None,
                          k8s_service: K8sSerivce = Depends(get_k8s_service)
                          ) -> ResponseDeployments:
    try:
        deployments: dict = k8s_service.get_deployments(namespace)
        return ResponseDeployments(results=deployments.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch deployments: {str(e)}"
        )
