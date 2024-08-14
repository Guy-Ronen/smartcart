import datetime
import uuid

from smart_cart.schemas.token import TokenPayload
from smart_cart.schemas.user import User


def token_payload_factory(
    token_id: str = str(uuid.uuid4()),
    user_id: str = "user123",
    username: str = "John Doe",
    email: str = "john.doe@example.com",
    created_at: int = int(datetime.datetime.now().timestamp()),
    expires_at: int = int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp()),
):
    return TokenPayload(
        token_id=token_id,
        user_id=user_id,
        username=username,
        email=email,
        created_at=created_at,
        expires_at=expires_at,
    )


def user_factory(
    id: str = str(uuid.uuid4()),
    username: str = "john_doe",
    email: str = "john.doe@example.com",
    hashed_password: str = "hashed_password",
    first_name: str = "John",
    last_name: str = "Doe",
    created_at: int = int(datetime.datetime.now().timestamp()),
    updated_at: int = None,
    last_login: int = None,
    is_active: bool = True,
    is_superuser: bool = False,
    is_staff: bool = False,
):
    return User(
        id=id,
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
