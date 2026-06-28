# Бизнес-логика Auth Service
from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, dto: RegisterRequest) -> UserPublic:
        """Регистрация нового пользователя"""
        existing_user = await self.user_repo.get_by_email(dto.email)
        if existing_user:
            raise UserAlreadyExistsError()
        
        hashed_password = hash_password(dto.password)
        new_user = User(
            email=dto.email,
            password_hash=hashed_password,
            role="user"
        )
        created_user = await self.user_repo.create(new_user)
        return UserPublic.model_validate(created_user)
    
    async def login(self, email: str, password: str) -> TokenResponse:
        """Аутентификация пользователя, выпуск JWT"""
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        
        token = create_access_token(
            subject=user.id,
            role=user.role
        )
        return TokenResponse(access_token=token)
    
    async def me(self, user_id: int) -> UserPublic:
        """Получение профиля текущего пользователя"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return UserPublic.model_validate(user)