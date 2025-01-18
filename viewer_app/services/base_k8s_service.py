from typing import Protocol


class BaseSerivceK8s(Protocol):

    def __init__(self, client: any):
        ...

    def get_workloads():
        ...
