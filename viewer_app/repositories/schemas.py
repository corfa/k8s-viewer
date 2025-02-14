from dataclasses import dataclass


@dataclass
class EnvVarDB:
    name: str
    value: str


@dataclass
class DeploymentDB:
    image: str
    id: int = None
    namespace: str = None
