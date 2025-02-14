import os
from pyhocon import ConfigFactory
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_DIR = os.path.abspath(os.path.join(BASE_DIR, "../settings"))


def load_config(env: str = "local") -> dict:
    config_path = os.path.join(SETTINGS_DIR, f"{env}.conf")
    return ConfigFactory.parse_file(config_path).as_plain_ordered_dict()


class DBSettings(BaseModel):
    host: str
    user: str
    password: str
    db_name: str
    port: int
    max_pool: int = 10
    min_pool: int = 1


class K8sSettings(BaseModel):
    context: str
    path: str = "~/.kube/config"
    use_fake_client: bool = False


class AppConfig(BaseModel):
    db: DBSettings
    k8s: K8sSettings


config_dict = load_config(os.getenv('ENV', 'local'))
app_config = AppConfig(**config_dict)

k8s_settings = app_config.k8s
db_settings = app_config.db
