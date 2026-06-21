from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Системные логи при старте контейнера веб-части
    print(f"Запуск веб-интерфейса {settings.APP_NAME}...")
    yield
    print(f"Остановка веб-интерфейса {settings.APP_NAME}...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Bot Service API and Health Status",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/health", tags=["System"])
async def healthcheck():
    """Служебный эндпоинт для проверки статуса контейнера (healthcheck)"""
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "environment": settings.ENV
    }
