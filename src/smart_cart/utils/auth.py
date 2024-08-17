import datetime
import uuid

import bcrypt
import jwt

from smart_cart.models.token import TokenPayload
from smart_cart.models.user import User
from smart_cart.utils.settings import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(user: User) -> str:
    token_payload = TokenPayload(
        token_id=str(uuid.uuid4()),
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        created_at=int(datetime.datetime.now().timestamp()),
        expires_at=int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp()),
    )

    encoded_jwt = jwt.encode(token_payload.model_dump(), settings.token_payload_secret_key, algorithm="HS256")

    return encoded_jwt