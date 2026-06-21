import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.schemas import UserCreate, Token
from app.database import Base

# Настройка in-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Подменяем зависимость get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Успешные сценарии
def test_register_user():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "test123", "role": "user"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_login_user():
    # Регистрируем пользователя
    client.post("/auth/register", json={"email": "user@example.com", "password": "test123", "role": "user"})
    # Логинимся
    response = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "test123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_me():
    # Получаем токен
    register_response = client.post(
        "/auth/register",
        json={"email": "me@example.com", "password": "test123", "role": "user"}
    )
    token = register_response.json()["access_token"]
    # Проверяем доступ к /auth/me
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"

# Негативные сценарии
def test_duplicate_email():
    client.post("/auth/register", json={"email": "dup@example.com", "password": "test123", "role": "user"})
    response = client.post(
        "/auth/register",
        json={"email": "dup@example.com", "password": "test123", "role": "user"}
    )
    assert response.status_code == 409

def test_wrong_password():
    client.post("/auth/register", json={"email": "wrong@example.com", "password": "test123"})
    response = client.post(
        "/auth/login",
        data={"username": "wrong@example.com", "password": "wrong_pass"}
    )
    assert response.status_code == 401

def test_invalid_token():
    response = client.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
