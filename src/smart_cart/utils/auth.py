import datetime
import uuid

import bcrypt
import jwt

from smart_cart.models.token import TokenPayload
from smart_cart.models.user import User as UserModel
from smart_cart.repositories.users import User
from smart_cart.utils.constants import DATETIME_NOW, DATETIME_NOW_TIMESTAMP
from smart_cart.utils.settings import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(user: User | UserModel) -> str:
    token_payload = TokenPayload(
        jti=str(uuid.uuid4()),
        sub=user.user_id,
        iat=DATETIME_NOW_TIMESTAMP,
        exp=int((DATETIME_NOW + datetime.timedelta(days=1)).timestamp()),
    )

    encoded_jwt = jwt.encode(
        token_payload.model_dump(), settings.token_payload_secret_key, algorithm=settings.hashing_algorithm
    )

    return encoded_jwt
