import asyncio
import os

from api.dependencies import get_k8s_client, get_service_deployment, get_deployments_repositories, get_envs_repositories
from kube.client import K8sClient
from repositories.deployment_repo import DeploymentRepository
from repositories.envs_repo import EnvRepository
from core.db import database

INTERVAL = int(os.getenv("SYNC_INTERVAL", 1800))


async def sync_deployments():
    await database.connect()
    client_k8s: K8sClient = get_k8s_client()
    deployment_repo: DeploymentRepository = get_deployments_repositories()
    env_repo: EnvRepository = get_envs_repositories()

    service_deployemnt = get_service_deployment(deployment_repo, client_k8s, env_repo)

    while True:
        data = service_deployemnt.get_deployments_from_cluster()
        await service_deployemnt.insert_deployments(data)
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(sync_deployments())
