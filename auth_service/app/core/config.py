# Настройка приложения и конфигурация
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "auth-service"
    ENV: str = "local"
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SQLITE_PATH: str = "./auth.db"

    @property
    def database_url(self) -> str:
        import os
        abs_path = os.path.abspath(self.SQLITE_PATH)
        return f"sqlite+aiosqlite:////{abs_path}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()