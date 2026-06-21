# Описание pydantic-схем для регистрации и токенов
from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Пароль должен быть не менее 8 символов")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
