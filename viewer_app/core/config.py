import os
from pyhocon import ConfigFactory
from pydantic import BaseModel
import psycopg2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_DIR = os.path.abspath(os.path.join(BASE_DIR, "../settings"))


def load_config(env: str = "local") -> ConfigFactory:
    config_path = os.path.join(SETTINGS_DIR, f"{env}.conf")
    return ConfigFactory.parse_file(config_path)


config: ConfigFactory = load_config(os.getenv('ENV', 'local'))


class DBSettings(BaseModel):
    host: str = config.get_string("db.host")
    user: str = config.get_string("db.user")
    password: str = config.get_string("db.password")
    db_name: str = config.get_string("db.db_name")
    port: str = config.get_string("db.port")
    max_pool: str = config.get_int("db.max_pool", 10)
    min_pool: str = config.get_int("db.min_pool", 1)

    @property
    def cursor(self):
        conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port="5432"
        )
        return conn, conn.cursor()


class K8sSettings(BaseModel):
    context: str = config.get_string("k8s.context")
    path: str = config.get_string("k8s.path", "~/.kube/config")
    use_fake_client: bool = config.get_bool("k8s.use_fake_client", False)


k8s_settings = K8sSettings()
db_settings = DBSettings()
