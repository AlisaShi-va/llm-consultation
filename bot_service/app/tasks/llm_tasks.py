import asyncio
from aiogram import Bot
from app.infra.celery_app import celery_app
from app.core.config import settings
from app.services.openrouter_client import OpenRouterClient, OpenRouterClientError


async def _execute_llm_request(tg_chat_id: int, prompt: str):
    """Вспомогательная асинхронная функция для работы внутри Celery"""
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    client = OpenRouterClient()

    try:
        # Отправляем уведомление, что бот думает
        await bot.send_chat_action(chat_id=tg_chat_id, action="typing")

        # Получаем ответ от нейросети
        llm_response = await client.get_completion(prompt)

        # Отправляем результат пользователю
        await bot.send_message(chat_id=tg_chat_id, text=llm_response)

    except OpenRouterClientError as exc:
        await bot.send_message(
            chat_id=tg_chat_id,
            text="Не удалось получить ответ от нейросети, попробуйте позже."
        )
        print(f"[Celery Task Error]: {exc}")
    except Exception as exc:
        await bot.send_message(
            chat_id=tg_chat_id,
            text="Произошла внутренняя ошибка при обработке запроса."
        )
        print(f"[Celery Unexpected Error]: {exc}")
    finally:
        # Закрываем сессию бота в воркере
        await bot.session.close()


@celery_app.task(name="app.tasks.llm_tasks.llm_request")
def llm_request(tg_chat_id: int, prompt: str):
    """
    Фоновая задача Celery для обработки запросов к LLM.
    Запускает асинхронный цикл для выполнения сетевых запросов
    """
    asyncio.run(_execute_llm_request(tg_chat_id, prompt))
