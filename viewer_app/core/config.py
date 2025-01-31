import os
from dataclasses import dataclass

from pyhocon import ConfigFactory
from pydantic import BaseModel


def load_config(env: str = "dev") -> ConfigFactory:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'configs-app', f'{env}.conf')
    return ConfigFactory.parse_file(config_path)


config: ConfigFactory = load_config(os.getenv('ENV', 'dev'))


@dataclass
class TestClient:
    quantity: int = 10
    set_envs_names: tuple = ()
    set_envs_values: tuple = ()
    set_images: tuple = ()


class K8sSettings(BaseModel):
    context: str = config.get_string("k8s.context")
    path: str = config.get_string("k8s.path", "~/.kube/config")
    use_fake_client: bool = config.get_bool("k8s.use_fake_client", False)

    test_client: TestClient = TestClient(**config.get_config("k8s.test_client"))


k8s_settings = K8sSettings()
