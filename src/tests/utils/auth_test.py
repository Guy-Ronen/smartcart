from uuid import UUID

import bcrypt
import jwt

from smart_cart.utils.auth import create_access_token, hash_password, verify_password
from smart_cart.utils.factories import user_factory
from smart_cart.utils.settings import settings


def test_hash_password():
    password = "password"
    hashed_password = hash_password(password)

    assert bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def test_verify_password():
    password = "password"
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    assert verify_password(password, hashed_password) is True
    assert verify_password("wrong_password", hashed_password) is False


def test_create_access_token():
    user = user_factory()

    token = create_access_token(user)

    decoded_token = jwt.decode(token, settings.token_payload_secret_key, algorithms=[settings.hashing_algorithm])

    assert isinstance(UUID(decoded_token["jti"]), UUID)
    assert decoded_token["sub"] == user.user_id
    assert decoded_token["created_at"] is not None
    assert decoded_token["expires_at"] is not None
