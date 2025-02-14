from services.k8s_service import K8sSerivce
from kube.client import K8sClient
from kube.schemas import Deployment as k8sDeployment
from services.domain.deployments import Deployment, DeploymentsSnapshotCluster

from repositories.schemas import DeploymentDB, EnvVarDB
from repositories.deployment_repo import DeploymentRepository
from repositories.envs_repo import EnvRepository


class DeploymentService(K8sSerivce):
    def __init__(self, client: K8sClient, deployment_repo: DeploymentRepository, env_repo: EnvRepository) -> DeploymentsSnapshotCluster:
        self._clinet_k8s = client
        self._deployment_repo = deployment_repo
        self._env_repo = env_repo

    def get_deployments_from_cluster(self, namespace: str | None = None) -> DeploymentsSnapshotCluster:
        data_deployments: list[k8sDeployment] = self._clinet_k8s.get_deployments(namespace)
        count_deployments: int = len(data_deployments)

        result_data: list = []

        for k8s_deployment in data_deployments:
            result_data.append(Deployment(**k8s_deployment.model_dump()))

        if namespace:
            return DeploymentsSnapshotCluster(namespaces=namespace,
                                              count=count_deployments,
                                              deployments=result_data)
        return DeploymentsSnapshotCluster(deployments=result_data, count=count_deployments)

    async def insert_deployments(self, deployments_snapshot: DeploymentsSnapshotCluster) -> None:
        for deployment in deployments_snapshot.deployments:
            repo_deployment = DeploymentDB(image=deployment.image)
            deployment_id = await self._deployment_repo.insert_deployment(repo_deployment,
                                                                          deployments_snapshot.namespaces,
                                                                          deployments_snapshot.time_response)

            if deployment.envs:
                envs_list = [EnvVarDB(name=env.get("name"),
                             value=env.get("value")) for env in deployment.envs]
                await self._env_repo.insert_envs(deployment_id, envs_list)

    async def get_deployments(self, namespace: str | None) -> DeploymentsSnapshotCluster:
        data_deployments = await self._deployment_repo.get_deployments(namespace)
        deployments_list = []
        for deployemt_db in data_deployments:
            deployments_list.append(Deployment(id=deployemt_db.id,
                                               image=deployemt_db.image))

        deployment_ids: list[int] = [dep.id for dep in deployments_list]

        env_map = await self._env_repo.get_envs_by_deployment(deployment_ids)

        for deployment in deployments_list:
            deployment.envs = env_map.get(deployment.id, [])

        return DeploymentsSnapshotCluster(deployments=deployments_list, count=len(data_deployments))
