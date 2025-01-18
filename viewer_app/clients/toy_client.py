import json

from clients.base_client import BaseClient
from core.config import K8sSettings


class ToyClients(BaseClient):

    def __init__(self, settings_k8s: K8sSettings) -> None:
        self.settings_k8s = settings_k8s
        self.toy_data = self.__read_file_data()

    def __read_file_data(self) -> dict:
        with open(self.settings_k8s.toy_data_path) as f:
            data = json.load(f)
        return data

    def get_deployments(self, namespace: str = None) -> dict[str, str]:
        pass
