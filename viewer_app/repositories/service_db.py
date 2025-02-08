from repositories.deployment_repo import DeploymentRepository
from services.domain.deployments import DeploymentsSnapshot, Deployment
from repositories.schemas import Deployment as DbDeployment, EnvVar as DbEnvVar


class DbService:
    def __init__(self, deployment_repo: DeploymentRepository):
        self._deployment_repo: DeploymentRepository = deployment_repo

    def insert_deployments(self, deployments_snapshot: DeploymentsSnapshot) -> None:
        for deployment in deployments_snapshot.deployments:
            envs_list: list = []
            for env in deployment.envs:
                envs_list.append(DbEnvVar(name=env.get("name"), value=env.get("value")))

            repo_deployment = DbDeployment(image=deployment.image, envs=envs_list)
            self._deployment_repo.insert_deployment(repo_deployment,
                                                    deployments_snapshot.namespaces,
                                                    str(deployments_snapshot.time_response))

    def get_deployments(self, namespace: str | None) -> DeploymentsSnapshot:
        data_deployments: list = self._deployment_repo.get_deployments(namespace)
        count_deployments: int = len(data_deployments)
        result_data: list = []

        for deployment in data_deployments:
            envs_list: list = []
            for env in deployment.envs:
                envs_list.append({"name": env.name, "value": env.value})
            result_data.append(Deployment(image=deployment.image, envs=envs_list))

        return DeploymentsSnapshot(deployments=result_data, count=count_deployments)
