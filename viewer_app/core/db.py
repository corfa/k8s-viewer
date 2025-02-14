from core.config import db_settings
from databases import Database

database = Database(
    f"postgresql://{db_settings.user}:{db_settings.password}@{db_settings.host}:{db_settings.port}/{db_settings.db_name}"
)