import time
import os

from api.dependencies import get_k8s_service, get_k8s_client, get_db_service, get_deployments_repositories
from services.k8s_cluster import KubeService
from kube.client import K8sClient
from repositories.deployment_repo import DeploymentRepository
from repositories.service_db import DbService

INTERVAL = int(os.getenv("SYNC_INTERVAL", 1800))

client_k8s: K8sClient = get_k8s_client()
k8s_service: KubeService = get_k8s_service(client_k8s)

db_repo: DeploymentRepository = get_deployments_repositories()
db_service: DbService = get_db_service(db_repo)

while True:
    data = k8s_service.get_deployments()
    db_service.insert_deployments(data)
    time.sleep(INTERVAL)
