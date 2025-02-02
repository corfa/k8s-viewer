import os
from dataclasses import dataclass

from pyhocon import ConfigFactory
from pydantic import BaseModel


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_DIR = os.path.abspath(os.path.join(BASE_DIR, "../settings"))


def load_config(env: str = "local") -> ConfigFactory:
    config_path = os.path.join(SETTINGS_DIR, f"{env}.conf")
    return ConfigFactory.parse_file(config_path)


config: ConfigFactory = load_config(os.getenv('ENV', 'local'))


class K8sSettings(BaseModel):
    context: str = config.get_string("k8s.context")
    path: str = config.get_string("k8s.path", "~/.kube/config")
    use_fake_client: bool = config.get_bool("k8s.use_fake_client", False)


k8s_settings = K8sSettings()
