from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    app_name: str = "Watcher"
    app_env: str = "development"
    debug: bool = True

    database_url: str

    http_timeout_seconds: float = 15.0
    http_max_concurrency: int = 5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_setting() -> Setting:
    return Setting()
