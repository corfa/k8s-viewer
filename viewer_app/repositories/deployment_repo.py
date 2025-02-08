from repositories.database import Database
from repositories.schemas import Deployment, EnvVar


class DeploymentRepository:
    def insert_deployment(self, deployment: Deployment, namespace: None | str, time_response: str) -> None:
        conn = Database.get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO deployments (namespace, image, time_response) VALUES (%s, %s, %s) RETURNING id",
                (namespace, deployment.image, time_response),
            )
            deployment_id = cur.fetchone()[0]

            for env in deployment.envs:
                cur.execute(
                    "INSERT INTO envs (deployment_id, name, value) VALUES (%s, %s, %s)",
                    (deployment_id, env.name, env.value),
                )

            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")

    def get_deployments(self, namespace_filter: str = None) -> list[Deployment]:
        conn = Database.get_connection()
        cur = conn.cursor()
        try:
            query = """
                SELECT d.id, d.namespace, d.image, d.time_response, e.name, e.value
                FROM deployments d
                LEFT JOIN envs e ON d.id = e.deployment_id
            """
            if namespace_filter:
                query = f"{query} WHERE d.namespace = %s"

            cur.execute(query, (namespace_filter,) if namespace_filter else ())
            rows = cur.fetchall()
            deployments = {}

            for row in rows:
                dep_id, namespace, image, time_response, env_name, env_value = row

                if dep_id not in deployments:
                    deployments[dep_id] = Deployment(
                        id=dep_id,
                        namespace=namespace,
                        image=image,
                        time_response=time_response,
                        envs=[],
                    )

                if env_name and env_value:
                    deployments[dep_id].envs.append(EnvVar(name=env_name, value=env_value))
            return list(deployments.values())
        except Exception as e:
            print(f"Error: {e}")
            return []
