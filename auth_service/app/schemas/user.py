# Описание публичного представления пользователя
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    # Поддержка чтения данных
    model_config = {
        "from_attributes": True
    }
