# Зависимости FastAPI
from typing import AsyncGenerator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase

# Определяем, откуда брать токен для защищенных эндпоинтов
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для предоставления асинхронной сессии БД"""
    async with AsyncSessionLocal() as session:
        yield session

def get_users_repo(session: AsyncSession = Depends(get_db)) -> UserRepository:
    """Пользовательские репозитории"""
    return UserRepository(session)

def get_auth_uc(user_repo: UserRepository = Depends(get_users_repo)) -> AuthUseCase:
    """Бизнес-логика авторизации"""
    return AuthUseCase(user_repo)

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Зависимость для извлечения и валидации ID пользователя из JWT"""
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        from app.core.exceptions import InvalidTokenError
        raise InvalidTokenError()
    return int(str(user_id))