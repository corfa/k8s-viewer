from typing import Protocol


class K8sSerivce(Protocol):

    def __init__(self, client: any) -> None:
        ...

    def get_deployments_from_cluster(*args, **kwargs):
        ...

    def get_deployments(*args, **kwargs):
        ...

    def insert_deployment(*args, **kwargs):
        ...
