# Проверка токена
from jose import JWTError, jwt
from datetime import datetime, timezone
from typing import Any, Dict
from app.core.config import settings

class TokenValidationError(Exception):
    """Базовое исключение для ошибок валидации токена в боте"""
    pass

class TokenExpiredValidationError(TokenValidationError):
    """Исключение для истекшего токена"""
    pass

def decode_and_validate(token: str) -> dict:
    """Валидирует JWT (проверяет подпись и срок действия).
    Возвращает payload в случае успеха или выбрасывает исключение"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG]
        )
        # Доп. проверка exp
        exp = payload.get("exp")
        if exp and datetime.now(timezone.utc).timestamp() > exp:
            raise TokenExpiredValidationError("Срок действия токена истек")
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredValidationError("Срок действия токена истек")
    except JWTError:
        raise TokenValidationError("Некорректный или поврежденный токен")