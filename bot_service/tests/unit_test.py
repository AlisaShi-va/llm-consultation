import pytest
from jose import jwt
from app.core.jwt import decode_and_validate

def test_decode_and_validate():
    secret = "test_secret"
    payload = {"sub": "user123"}
    token = jwt.encode(payload, secret, algorithm="HS256")
    decoded = decode_and_validate(token)
    assert decoded["sub"] == "user123"

def test_invalid_token():
    with pytest.raises(ValueError):
        decode_and_validate("invalid_token")
