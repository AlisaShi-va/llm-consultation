# Создание асинхронного engine SQLAlchemy и фабрики сессий 
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSessionLocal,
    expire_on_commit=False,
    future=True,
    autoflush=False,
    autocommit=False
)
