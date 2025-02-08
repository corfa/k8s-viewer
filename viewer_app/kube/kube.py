from kubernetes import client as k8s_client, config as k8s_config
from kubernetes.client.api.apps_v1_api import AppsV1Api
from kubernetes.client.api.batch_v1_api import BatchV1Api

from kube.client import K8sClient
from core.config import K8sSettings
from kube.schemas import Deployment, Environment


class KubernetesK8sClient(K8sClient):

    def __init__(self, settings_k8s: K8sSettings) -> None:
        self.settings_k8s = settings_k8s
        self._clinet_k8s = self.__init_cluster_clinet()

        self._apps_v1: AppsV1Api = self._clinet_k8s.AppsV1Api()
        self._batch_v1: BatchV1Api = self._clinet_k8s.BatchV1Api()

    def __init_cluster_clinet(self) -> any:
        try:
            k8s_config.load_incluster_config()
        except k8s_config.ConfigException:
            k8s_config.load_kube_config(config_file=self.settings_k8s.path,
                                        context=self.settings_k8s.context)
        return k8s_client

    def get_deployments(self, namespace: str | None = None) -> list[Deployment]:
        if namespace:
            data: dict = self._apps_v1.list_namespaced_deployment(namespace=namespace).to_dict()
        else:
            data: dict = self._apps_v1.list_deployment_for_all_namespaces().to_dict()

        deployements_list = []
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
