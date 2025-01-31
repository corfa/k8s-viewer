from fastapi import Depends

from services.cluster_k8s_service import ClusterK8sService
from clients import k8s_clients, fake_client
from clients.base_client import BaseClient
from core.config import k8s_settings


def get_k8s_client() -> BaseClient:
    if k8s_settings.use_fake_client:
        return fake_client.FakeClients(k8s_settings)
    else:
        return k8s_clients.K8sClients(k8s_settings)


def get_k8s_service(client: BaseClient = Depends(get_k8s_client)):

    return ClusterK8sService(client)
