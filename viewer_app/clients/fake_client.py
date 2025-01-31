import random

from clients.base_client import BaseClient
from core.config import K8sSettings
from clients.schemas.deployment import Deployment, Environment


def create_test_deployment(settings_k8s: K8sSettings) -> Deployment:
    set_envs_name: list = settings_k8s.test_client.set_envs_names
    set_envs_values: list = settings_k8s.test_client.set_envs_values
    set_images: list = settings_k8s.test_client.set_images

    return Deployment(image=set_images[random.randint(0, len(set_images)-1)],
                      envs=[Environment(
                            name=set_envs_name[random.randint(0, len(set_envs_name)-1)],
                            value=set_envs_values[random.randint(0, len(set_envs_values)-1)])])


def create_set_deployments(settings_k8s: K8sSettings,
                           quantity: int = 10) -> list[Deployment]:
    return [create_test_deployment(settings_k8s) for _ in range(quantity)]


class FakeClients(BaseClient):
    def __init__(self, settings_k8s: K8sSettings) -> None:
        self.settings_k8s = settings_k8s

    def get_deployments(self, namespace: str = None) -> list[Deployment]:
        return create_set_deployments(self.settings_k8s,
                                      self.settings_k8s.test_client.quantity)
