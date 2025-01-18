import os

from pyhocon import ConfigFactory
from pydantic_settings import BaseSettings


def load_config(env: str = "dev") -> ConfigFactory:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    config_path = os.path.join(current_dir, '..', 'configs', f'{env}.conf')
    return ConfigFactory.parse_file(config_path)


config: ConfigFactory = load_config(os.getenv('ENV', 'dev'))


class K8sSettings(BaseSettings):
    context: str = config.get_string("k8s.context", None)
    path: str = config.get_string("k8s.path", "~/.kube/config")
    toy_data_path: str = config.get_string("k8s.toy_data_path", "")


k8s_settings = K8sSettings()
