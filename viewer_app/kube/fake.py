import random

from kube.client import K8sClient
from core.config import K8sSettings
from kube.schemas import Deployment, Environment


def create_test_deployment() -> Deployment:
    set_envs_name: list = ["HOST_API", "DATABASE_NAME", "PORT", "DATABASE_USER", "TOKEN"]

    set_envs_values: list = ["localhost", "prod_database", "8080", "postgres",
                             "23954e2e-cfdb-403c-a186-df0b71c50eef"]
    set_images: list = ["postgres:latest", "nginx:dev", "flows-backend:stable",
                        "worker-celery:stable", "rabbitmq:dev"]

    return Deployment(image=set_images[random.randint(0, len(set_images)-1)],
                      envs=[Environment(
                            name=set_envs_name[random.randint(0, len(set_envs_name)-1)],
                            value=set_envs_values[random.randint(0, len(set_envs_values)-1)])])


def create_set_deployments(quantity: int = 10) -> list[Deployment]:
    return [create_test_deployment() for _ in range(quantity)]


class FakeK8sClient(K8sClient):
    def __init__(self, settings_k8s: K8sSettings) -> None:
        self.settings_k8s = settings_k8s

    def get_deployments(self, namespace: str = None) -> list[Deployment]:
        return create_set_deployments()
