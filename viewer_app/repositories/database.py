from psycopg2 import pool
from core.config import db_settings


class Database:
    _pool = None

    @classmethod
    def init_pool(cls):
        if cls._pool is None:
            cls._pool = pool.SimpleConnectionPool(
                db_settings.min_pool, db_settings.max_pool,
                dbname=db_settings.db_name,
                user=db_settings.user,
                password=db_settings.password,
                host=db_settings.host,
                port=db_settings.port
            )

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.init_pool()
        return cls._pool.getconn()

    @classmethod
    def release_connection(cls, conn):
        cls._pool.putconn(conn)

    @classmethod
    def close_pool(cls):
        if cls._pool:
            cls._pool.closeall()
