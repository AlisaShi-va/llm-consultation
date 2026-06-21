import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, Chat, User
from app.bot.handlers import handle_user_prompt


@pytest.mark.asyncio
async def test_handle_user_prompt_dispatches_to_celery(mock_redis, mock_celery_task):
    """
    Проверка перенаправления сообщения пользователя в Celery при
    наличии валидного токена в Redis и мгновенный ответ хендлера
    """
    # Подготовка фейковых данных
    user_id = 123456789
    redis_key = f"tg_user:{user_id}:token"
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6InVzZXIiLCJleHAiOjE5OTk5OTk5OTl9.signature"

    # Запись токена в тестовую базу Redis
    await mock_redis.set(redis_key, fake_token)

    # Имитация входяще сообщения от пользователя в aiogram
    chat_mock = Chat(id=user_id, type="private")
    user_mock = User(id=user_id, is_bot=False, first_name="TestUser")

    # Создание мок сообщения aiogram
    message = Message(
        message_id=1,
        date=None,
        chat=chat_mock,
        from_user=user_mock,
        text="Расскажи мне про хемоинформатику"
    )

    # Мокаем метод асинхронного ответа самого бота
    message.answer = AsyncMock()

    # Запуск тестируемого хендлера
    await handle_user_prompt(message)

    # Проверка вызова задач Celery
    mock_celery_task.assert_called_once_with(
        tg_chat_id=user_id,
        prompt="Расскажи мне про квантовую физику"
    )

    # Проверка возвращения ответа
    message.answer.assert_called_once()
    assert "Ваш запрос принят в обработку" in message.answer.call_args[0][0]

