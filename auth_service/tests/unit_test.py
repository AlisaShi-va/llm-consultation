import pytest
from jose import jwt
from passlib.context import CryptContext
from app.core.security import pwd_context, create_access_token

# Тесты для хеширования паролей
def test_password_hashing():
    password = "test_password"
    hashed = pwd_context.hash(password)
    assert hashed != password  # Хеш не равен исходному паролю
    assert pwd_context.verify(password, hashed)  # Верный пароль, проходит верификацию
    assert not pwd_context.verify("wrong_password", hashed)  # Неверный пароль

# Тесты для JWT
def test_jwt_creation_and_decoding():
    payload = {"sub": "user123", "role": "user"}
    token = create_access_token(payload)
    decoded = jwt.decode(token, "test_secret", algorithms=["HS256"])
    assert decoded["sub"] == "user123"
    assert decoded["role"] == "user"
    assert "iat" in decoded  # Время создания 
    assert "exp" in decoded  # Время истечения 
