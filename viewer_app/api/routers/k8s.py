from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_k8s_service
from services.cluster_k8s_service import ClusterK8sService
from models.response_deployments import DeploymentsResponse


router = APIRouter()


@router.get("/deployments")
async def get_deployments(namespace: str | None = None,
                          k8s_service: ClusterK8sService = Depends(get_k8s_service)
                          ) -> DeploymentsResponse:
    try:
        deployments = k8s_service.get_deployments(namespace)
        if namespace is None:
            namespace = 'all-ns'
        return DeploymentsResponse(namespace=namespace,
                                   deployments=deployments)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch deployments: {str(e)}"
        )
