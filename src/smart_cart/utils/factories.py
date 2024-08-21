import datetime
import uuid
from typing import Optional

from smart_cart.models.token import TokenPayload
from smart_cart.models.user import User, UserSignUp
from smart_cart.utils.constants import DATETIME_NOW, DATETIME_NOW_TIMESTAMP


def token_payload_factory(
    token_id: Optional[str] = None,
    user_id: str = "user123",
    username: str = "John Doe",
    email: str = "john.doe@example.com",
    created_at: Optional[int] = None,
    expires_at: Optional[int] = None,
):
    token_id = token_id or str(uuid.uuid4())
    created_at = created_at or DATETIME_NOW_TIMESTAMP
    expires_at = expires_at or int((DATETIME_NOW + datetime.timedelta(days=1)).timestamp())

    return TokenPayload(
        token_id=token_id,
        user_id=user_id,
        username=username,
        email=email,
        created_at=created_at,
        expires_at=expires_at,
    )


def user_signup_factory(
    username: str = "john_doe",
    email: Optional[str] = None,
    password: str = "password",
    first_name: str = "John",
    last_name: str = "Doe",
):
    email = email or f"user_{uuid.uuid4()}@example.com"
    return UserSignUp(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )


def user_factory(
    user_id: Optional[str] = None,
    username: str = "john_doe",
    email: Optional[str] = None,
    hashed_password: str = "hashed_password",
    first_name: str = "John",
    last_name: str = "Doe",
    created_at: Optional[int] = None,
    updated_at: Optional[int] = None,
    last_login: Optional[int] = None,
    is_active: bool = True,
    is_superuser: bool = False,
    is_staff: bool = False,
):
    user_id = user_id or str(uuid.uuid4())
    email = email or f"user_{uuid.uuid4()}@example.com"
    created_at = created_at or DATETIME_NOW_TIMESTAMP

    return User(
        user_id=user_id,
        username=username,
        email=email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        created_at=created_at,
        updated_at=updated_at,
        last_login=last_login,
        is_active=is_active,
        is_superuser=is_superuser,
        is_staff=is_staff,
    )
