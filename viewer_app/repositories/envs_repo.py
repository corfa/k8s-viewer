from repositories.schemas import EnvVarDB
from core.db import database


class EnvRepository:
    async def insert_envs(self, deployment_id: int, envs: list[EnvVarDB]) -> None:
        query = """
            INSERT INTO envs (deployment_id, name, value) 
            VALUES (:deployment_id, :name, :value)
        """
        values = [{"deployment_id": deployment_id, "name": env.name, "value": env.value} for env in envs]

        if values:
            await database.execute_many(query=query, values=values)

    async def get_envs_by_deployment(self, deployment_ids: list[int]) -> dict[int, list[EnvVarDB]]:
        if not deployment_ids:
            return {}

        query = """
            SELECT deployment_id, name, value
            FROM envs
            WHERE deployment_id = ANY(:deployment_ids)
        """
        values = {"deployment_ids": deployment_ids}
        rows = await database.fetch_all(query=query, values=values)

        env_map = {}
        for row in rows:
            if row["deployment_id"] not in env_map:
                env_map[row["deployment_id"]] = []
            env_map[row["deployment_id"]].append(EnvVarDB(name=row["name"], value=row["value"]))

        return env_map
