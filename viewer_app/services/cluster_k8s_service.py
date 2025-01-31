from services.base_k8s_service import BaseSerivceK8s
from clients.base_client import BaseClient

from services.domain.deployments import DeploymentsSnapshot
from schemes.deployment import Deployment


class ClusterK8sService(BaseSerivceK8s):
    def __init__(self, client: BaseClient) -> None:
        self._clinet_k8s = client

    def get_deployments(self, namespace: str | None = None) -> list[DeploymentsSnapshot]:
        data_deployments: list[Deployment] = self._clinet_k8s.get_deployments(namespace)
        count_deployment = len(data_deployments)
        if namespace:
            return DeploymentsSnapshot(namespaces=namespace,
                                       count=count_deployment,
                                       deployments=data_deployments)
        return DeploymentsSnapshot(deployments=data_deployments, count=count_deployment)
