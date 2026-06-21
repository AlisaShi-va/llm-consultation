import pytest
from unittest.mock import patch, MagicMock
from fakeredis import FakeRedis
from aiogram import types
from app.bot.handlers import set_token, handle_text
from app.tasks.llm_tasks import llm_request

@pytest.fixture
def fake_message():
    return types.Message(
        bot=MagicMock(),
        chat=types.Chat(id=123),
        date=0,
        text="test_prompt"
    )

@pytest.fixture
def fake_redis():
    return FakeRedis()

@patch("app.bot.handlers.get_redis")
def test_set_token_success(mock_get_redis, fake_message, fake_redis):
    mock_get_redis.return_value = fake_redis
    with patch("app.core.jwt.decode_and_validate") as mock_decode:
        mock_decode.return_value = {"sub": "user123"}
        set_token(fake_message, MagicMock())
        assert fake_redis.get("user:123") is not None

@patch("app.bot.handlers.get_redis")
def test_no_token_rejected(mock_get_redis, fake_message, fake_redis):
    mock_get_redis.return_value = fake_redis
    with patch("app.bot.handlers.decode_and_validate") as mock_decode:
        mock_decode.side_effect = ValueError("Invalid token")
        response = handle_text(fake_message)
        assert "Токен не найден" in response.text

@patch("app.bot.handlers.get_redis")
@patch("app.bot.handlers.llm_request.delay")
def test_text_with_token(mock_llm_request, mock_get_redis, fake_message, fake_redis):
    mock_get_redis.return_value = fake_redis
    fake_redis.set("user:123", "valid_token")
    handle_text(fake_message)
    mock_llm_request.delay.assert_called_once_with("test_prompt", 123)
