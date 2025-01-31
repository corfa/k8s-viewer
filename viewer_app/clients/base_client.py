from typing import Protocol

from clients.schemas.deployment import Deployment


class BaseClient(Protocol):

    def __init__(self, settings: any) -> None:
        ...

    def get_deployments(namespace: str = None) -> Deployment:
        ...
