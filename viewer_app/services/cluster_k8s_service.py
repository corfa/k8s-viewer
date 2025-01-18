from services.base_k8s_service import BaseSerivceK8s
from clients.base_client import BaseClient
from schemes.deployment import Deployment, Environment


class ClusterK8sService(BaseSerivceK8s):
    def __init__(self, client: BaseClient) -> None:
        self._clinet_k8s = client

    def get_deployments(self, namespace: str) -> list[Deployment]:
        deployements_list = []
        data: dict = self._clinet_k8s.get_deployments(namespace)
        for item in data.get('items'):
            image = item['spec']['template']['spec']['containers'][0]['image']
            list_envs = []
            envs = item['spec']['template']['spec']['containers'][0]["env"]

            if envs is not None:
                for env in envs:
                    list_envs.append(Environment(name=env['name'],
                                                 value=env['value']))
            deployements_list.append(Deployment(image=image, envs=list_envs))

        return deployements_list
