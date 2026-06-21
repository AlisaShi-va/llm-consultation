# Реализация логики общения с пользователем
from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from app.infra.redis import get_redis
from app.core.jwt import decode_and_validate, TokenValidationError
from app.tasks.llm_tasks import llm_request

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Приветственное сообщение с инструкцией"""
    await message.answer(
        "👋 Привет! Я нейросетевой ассистент.\n\n"
        "Чтобы начать общение, вам нужно авторизоваться в **Auth Service**.\n"
        "Получите JWT-токен и отправьте его мне командой:\n"
        "`/token ВАШ_JWT_ТОКЕН`"
    )


@router.message(Command("token"))
async def cmd_save_token(message: types.Message, command: CommandObject):
    """Принимает JWT-токен от пользователя и привязывает к его Tg ID в Redis"""
    token = command.args
    if not token:
        await message.answer("❌ Пожалуйста, укажите токен после команды. Пример:\n`/token eyJhbGci...`")
        return

    try:
        # Валидируем токен перед сохранением
        payload = decode_and_validate(token)
        exp = payload.get("exp")

        # Получаем клиент Redis
        redis_client = await get_redis()
        redis_key = f"tg_user:{message.from_user.id}:token"

        # Вычисляем время жизни токена (TTL)
        import time
        current_time = int(time.time())
        ttl = int(exp - current_time) if exp else 3600

        if ttl <= 0:
            await message.answer("❌ Данный токен просрочен. Получите новый в Auth Service")
            return

        # Сохраняем токен в Redis с TTL
        await redis_client.set(redis_key, token, ex=ttl)
        await message.answer("✅ Авторизация прошла успешно! Теперь вы можете отправлять мне любые текстовые запросы")

    except TokenValidationError:
        await message.answer("❌ Некорректный токен. Проверьте правильность ввода")


@router.message()
async def handle_user_prompt(message: types.Message):
    """Обрабатывает текстовые запросы пользователей, проверяя авторизацию"""
    if not message.text:
        return

    redis_client = await get_redis()
    redis_key = f"tg_user:{message.from_user.id}:token"

    # Извлекаем токен из Redis
    token = await redis_client.get(redis_key)

    if not token:
        await message.answer("🔒 Доступ ограничен. Вы не авторизованы, используйте команду `/token <ваш_jwt>`")
        return

    try:
        # Валидируем подпись и срок действия токена
        decode_and_validate(token)

        # Токен валиден — отправляем тяжелую задачу генерации ответа в Celery
        llm_request.delay(tg_chat_id=message.chat.id, prompt=message.text)

        await message.answer("⏳ Ваш запрос принят в обработку. Нейросеть генерирует ответ...")

    except TokenValidationError:
        # Если токен просрочен
        await redis_client.delete(redis_key)
        await message.answer("🔒 Срок действия вашей сессии истек. Пожалуйста, получите новый токен в Auth Service.")