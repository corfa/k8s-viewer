from fastapi import Depends

from services.cluster_k8s_service import ClusterK8sService
from clients.k8s_clients import K8sClients
from core.config import k8s_settings


def get_k8s_client():
    return K8sClients(k8s_settings)


def get_k8s_service(client=Depends(get_k8s_client)):
    return ClusterK8sService(client)
