from fastapi import Depends

from services.deploymen_service import DeploymentService
from kube import fake, kube
from kube.client import K8sClient
from core.config import k8s_settings
from repositories.deployment_repo import DeploymentRepository
from repositories.envs_repo import EnvRepository


def get_deployments_repositories() -> DeploymentRepository:
    return DeploymentRepository()


def get_envs_repositories() -> EnvRepository:
    return EnvRepository()


def get_k8s_client() -> K8sClient:
    if k8s_settings.use_fake_client:
        return fake.FakeK8sClient(k8s_settings)
    else:
        return kube.KubernetesK8sClient(k8s_settings)


def get_service_deployment(deployment_repo: DeploymentRepository = Depends(get_deployments_repositories),
                           client: K8sClient = Depends(get_k8s_client),
                           envs_repo: EnvRepository = Depends(get_envs_repositories)) -> DeploymentService:
    return DeploymentService(client, deployment_repo, envs_repo)
