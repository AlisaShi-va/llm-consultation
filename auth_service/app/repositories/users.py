# Реализация репозитория доступа к пользователям
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        """Сохранение нового пользователя в БД"""
        user.email = user.email
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_by_email(self, email: str) -> Optional[User] | None:
        """Получение пользователя по email"""
        result = await self.session.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalars().first()
    
    async def get_by_id(self, user_id: int) -> Optional[User] | None:
        """Получение пользователя по ID"""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
