from kubernetes import client as k8s_client, config as k8s_config

from clients.base_client import BaseClient
from core.config import K8sSettings


class K8sClients(BaseClient):

    def __init__(self, settings_k8s: K8sSettings) -> None:
        self.settings_k8s = settings_k8s
        self._clinet_k8s = self.__init_cluster_clinet()

        self._apps_v1 = self._clinet_k8s.AppsV1Api()
        self._batch_v1 = self._clinet_k8s.BatchV1Api()

    def __init_cluster_clinet(self) -> any:
        try:
            k8s_config.load_incluster_config()
        except k8s_config.ConfigException:
            k8s_config.load_kube_config(config_file=self.settings_k8s.path,
                                        context=self.settings_k8s.context)
        return k8s_client

    def get_deployments(self, namespace: str = None) -> dict[str, str]:
        if namespace:
            return self._apps_v1.list_namespaced_deployment(namespace=namespace).to_dict()
        return self._apps_v1.list_deployment_for_all_namespaces().to_dict()
