from repositories.schemas import DeploymentDB
from core.db import database


class DeploymentRepository:
    async def insert_deployment(self, deployment: DeploymentDB, namespace: None | str, time_response: str) -> int:
        query = """
            INSERT INTO deployments (namespace, image, time_response)
            VALUES (:namespace, :image, :time_response)
            RETURNING id
        """
        values = {"namespace": namespace, "image": deployment.image, "time_response": time_response}
        async with database.transaction():
            deployment_id = await database.execute(query=query, values=values)
        return deployment_id

    async def get_deployments(self, namespace_filter: str = None) -> list[DeploymentDB]:
        query = """
            SELECT id, namespace, image, time_response
            FROM deployments
        """
        values = {}

        if namespace_filter:
            query += " WHERE namespace = :namespace"
            values["namespace"] = namespace_filter

        rows = await database.fetch_all(query=query, values=values)
        return [DeploymentDB(id=row["id"], namespace=row["namespace"], image=row["image"]) for row in rows]
