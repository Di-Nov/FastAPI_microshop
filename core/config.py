from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import BaseModel

# Для точного опредениения пути создания файлов (Путь рассположения проекта)
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    # echo: bool = False
    echo: bool = True  # Для вывода логов SQL при создании, только при отладке !!


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()


settings = Settings()
