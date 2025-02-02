from fastapi import Depends

from services.k8s_cluster import KubeService
from k8s import fake, kube
from k8s.client import K8sClient
from core.config import k8s_settings


def get_k8s_client() -> K8sClient:
    if k8s_settings.use_fake_client:
        return fake.FakeK8sClient(k8s_settings)
    else:
        return kube.KubernetesK8sClient(k8s_settings)


def get_k8s_service(client: K8sClient = Depends(get_k8s_client)) -> KubeService:

    return KubeService(client)
