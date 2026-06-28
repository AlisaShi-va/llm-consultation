import sys
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.bot.dispatcher import bot, get_dispatcher

dp = get_dispatcher()

@asynccontextmanager
async def lifespan(_app: FastAPI):
    is_celery_worker = any("celery" in arg for arg in sys.argv)
    bot_polling_task = None

    if not is_celery_worker:
        bot_polling_task = asyncio.create_task(dp.start_polling(bot, skip_updates=True))
        print("Telegram-бот успешно запущен")
    else:
        print("Запуск Telegram пропущен")
    yield

    if bot_polling_task and not is_celery_worker:
        print("Остановка работы бота...")
        await dp.stop_polling()
        bot_polling_task.cancel()
        await bot.session.close()

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
