from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from app.core.config import settings
from app.bot.handlers import router as main_router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.telegram import TelegramAPIServer

# Создаем зеркало для работы без ВПН
tg_mirror = TelegramAPIServer.from_base("https://tgproxy.today")
custom_session = AiohttpSession(api=tg_mirror)

# Инстанс бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, session=custom_session)

def get_dispatcher() -> Dispatcher:
    """Собирает и возвращает настроенный диспетчер aiogram"""
    dp = Dispatcher()
    # Подключаем роутер с хендлерами
    dp.include_router(main_router)
    return dp
