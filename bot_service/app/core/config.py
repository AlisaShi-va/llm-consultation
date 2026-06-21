# Настройки Bot Service
from pydantic_settings import BaseSettings, SettingConfigDict

class Settings(BaseSettings):
    APP_NAME: str= "bot-service"
    ENV: str = "local"
    # Настройки Tg
    TELEGRAM_BOT_TOKEN: str
    # Валидация JWT
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    # Инфраструктура
    REDIS_URL: str = "redis://redis:6379/0"
    RABBITMQ_URL: str= "amqp://guest:guest@rabbitmq:5672//"
    # Настройки интеграции с LLM
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "stepfun/step-3.5-flash:free"

    model_config = SettingConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
