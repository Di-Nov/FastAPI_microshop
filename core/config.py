from pathlib import Path

from pydantic_settings import BaseSettings

# Для точного опредениения пути создания файлов (Путь рассположения проекта)
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseSettings):
    url_db: str = f"sqlite+aiosqlite:///{DB_PATH}"
    db_echo: bool = False
    # db_echo: bool = True  # Для вывода логов SQL при создании, только при отладке !!


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()


settings = Settings()
