from services.k8s_service import K8sSerivce
from k8s.client import K8sClient
from k8s.schemas import Deployment as k8sDeployment
from services.domain.deployments import Deployment, DeploymentsSnapshot


class KubeService(K8sSerivce):
    def __init__(self, client: K8sClient) -> None:
        self._clinet_k8s = client

    def get_deployments(self, namespace: str | None = None) -> DeploymentsSnapshot:
        data_deployments: list[k8sDeployment] = self._clinet_k8s.get_deployments(namespace)
        count_deployments: int = len(data_deployments)

        result_data: list = []

        for k8s_deployment in data_deployments:
            result_data.append(Deployment(**k8s_deployment.model_dump()))

        if namespace:
            return DeploymentsSnapshot(namespaces=namespace,
                                       count=count_deployments,
                                       deployments=result_data)
        return DeploymentsSnapshot(deployments=result_data, count=count_deployments)
