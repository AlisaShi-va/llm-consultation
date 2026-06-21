from celery import Celery
from app.core.config import settings

celery_app= Celery(
    "bot_service",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL
)

celery_app.autodiscover_tasks(["app.tasks"])

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=300,  # Лимит на выполнение задачи - 5 минут
    worker_prefetch_multiplier=1
)
