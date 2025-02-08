from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_db_service
from api.schemas.response_deployments import ResponseDeployments
from repositories.service_db import DbService

router = APIRouter()


@router.get("/deployments")
async def get_deployments(namespace: str | None = None,
                          db_service: DbService = Depends(get_db_service)
                          ) -> ResponseDeployments:
    try:
        deployments: dict = db_service.get_deployments(namespace)
        print(deployments)
        return ResponseDeployments(results=deployments.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch deployments: {str(e)}"
        )
