import uuid
from typing import Optional

from smart_cart.models.user import User, UserLogin, UserSignUp
from smart_cart.utils.constants import (
    FIXED_EMAIL,
    FIXED_HASHED_PASSWORD,
    FIXED_TIMESTAMP,
    FIXED_USER_ID,
)


def user_signup_factory(
    email: Optional[str] = None,
    password: str = "password",
    first_name: str = "John",
    last_name: str = "Doe",
):
    email = email or f"user_{uuid.uuid4()}@example.com"
    return UserSignUp(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )


def user_factory(
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    hashed_password: Optional[str] = None,
    first_name: str = "John",
    last_name: str = "Doe",
    created_at: Optional[int] = None,
    updated_at: Optional[int] = None,
    last_login: Optional[int] = None,
    is_active: bool = False,
    is_superuser: bool = False,
    is_staff: bool = False,
):
    user_id = user_id or FIXED_USER_ID
    email = email or FIXED_EMAIL
    hashed_password = hashed_password or FIXED_HASHED_PASSWORD
    created_at = created_at or FIXED_TIMESTAMP

    return User(
        user_id=user_id,
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


def user_login_factory(email: Optional[str] = None, password: str = "password"):
    email = email or f"user_{uuid.uuid4()}@example.com"

    return UserLogin(email=email, password=password)
