from aiogram import Bot, Dispatcher
from app.core.config import settings
from app.bot.handlers import router as main_router

# Инстанс бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

def get_dispatcher() -> Dispatcher:
    """Собирает и возвращает настроенный диспетчер aiogram"""
    dp = Dispatcher()

    # Подключаем роутер с хендлерами
    dp.include_router(main_router)

    return dp
