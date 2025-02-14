from typing import Protocol

from kube.schemas import Deployment


class K8sClient(Protocol):

    def __init__(self, settings: any) -> None:
        ...

    def get_deployments(namespace: str = None) -> Deployment:
        ...
