from typing import Protocol


class BaseClient(Protocol):

    def __init__(self, settings: any) -> None:
        ...

    def get_deployments(namespace: str = None) -> dict:
        ...
