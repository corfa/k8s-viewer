from pydantic import BaseModel
from typing import Union


class Environment(BaseModel):
    name: str
    value: Union[str, int, float, None]


class Deployment(BaseModel):
    image: str
    envs: list[Environment]
