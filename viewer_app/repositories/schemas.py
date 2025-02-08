from dataclasses import dataclass
from typing import List


@dataclass
class EnvVar:
    name: str
    value: str


@dataclass
class Deployment:
    image: str
    envs: List[EnvVar]
    time_response: str
    id: int = None
    namespace: str = None
