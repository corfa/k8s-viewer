from typing import Protocol

from k8s.schemas import Deployment


class K8sClient(Protocol):

    def __init__(self, settings: any) -> None:
        ...

    def get_deployments(namespace: str = None) -> Deployment:
        ...
