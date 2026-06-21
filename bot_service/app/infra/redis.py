# Единая точка получения redis-клиента
import redis.asyncio as redis
from app.core.config import settings

_redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True
)

async def get_redis() -> redis.Redis:
    return _redis_client