import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.db.session import get_db, engine
from app.db.models import Base
from app.schemas.auth import RegisterRequest

# Настройка тестовой БД
@pytest.fixture(scope="session")
async def async_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await engine.dispose()

client = TestClient(app)

@pytest.mark.asyncio
async def test_register_user():
    response = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "test123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"

@pytest.mark.asyncio
async def test_register_duplicate():
    response = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "test123"}
    )
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_login_success():
    client.post("/auth/register", json={"email": "user@example.com", "password": "test123"})
    response = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "test123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_me_endpoint():
    client.post("/auth/register", json={"email": "user@example.com", "password": "test123"})
    login_response = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "test123"}
    )
    token = login_response.json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
