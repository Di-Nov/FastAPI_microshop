from pathlib import Path

from pydantic_settings import BaseSettings

# Для точного опредениения пути создания файлов (Путь рассположения проекта)
BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    url_db: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = False  # Для вывода логов SQL при создании


settings = Settings()
