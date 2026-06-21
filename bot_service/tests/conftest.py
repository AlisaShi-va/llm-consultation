import pytest
import fakeredis.aio
from unittest.mock import AsyncMock


@pytest.fixture(autouse=True)
async def mock_redis(monkeypatch):
    """
    Подменяет реальный клиент Redis на in-memory базу fakeredis
    в модуле инфраструктуры на время выполнения тестов
    """
    fake_client = fakeredis.aio.FakeRedis(decode_responses=True)

    # Создаем асинхронный мок для функции get_redis
    async def mock_get_redis():
        return fake_client

    # Патчим единую точку входа получения Redis для хендлеров
    monkeypatch.setattr("app.infra.redis.get_redis", mock_get_redis)

    yield fake_client

    # Очищаем БД после каждого теста
    await fake_client.flushall()
    await fake_client.close()


@pytest.fixture
def mock_celery_task(monkeypatch):
    """Мокает вызов Celery-задачи для избежания подключения к RabbitMQ"""
    mock_delay = AsyncMock()
    monkeypatch.setattr("app.tasks.llm_tasks.llm_request.delay", mock_delay)
    return mock_delay
