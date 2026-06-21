# Описания HTTP-исключений
from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class BaseHTTPException(HTTPException):
    """Базовое исключение для всего Auth Service."""
    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL: str = "Внутренняя ошибка сервера"

    def __init__(
            self,
            detail: Optional[str] = None,
            headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=self.STATUS_CODE,
            detail=detail or self.DETAIL,
            headers=headers
        )

class UserAlreadyExistsError(BaseHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT,
    DETAIL = "Пользователь с таким email уже существует"

class InvalidCredentialsError(BaseHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED,
    DETAIL = "Некорректный логин или пароль"

class InvalidTokenError(BaseHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED,
    DETAIL = "Недействительный токен"

    def __init__(self, detail: Optional[str] = None):
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(detail=detail or self.DETAIL, headers=headers)

class TokenExpiredError(InvalidTokenError):
    DETAIL = "Срок действия токена истек"

class UserNotFoundError(BaseHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Пользователь не найден"

class PermissionDeniedError(BaseHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Недостаточно прав для выполнения операции"