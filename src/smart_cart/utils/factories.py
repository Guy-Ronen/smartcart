import datetime
import uuid
from typing import Optional

from smart_cart.models.receipt import Currency, Item, Market, Receipt
from smart_cart.models.token import TokenPayload
from smart_cart.models.user import User, UserLogin, UserSignUp
from smart_cart.utils.auth import hash_password
from smart_cart.utils.constants import DATETIME_NOW, DATETIME_NOW_TIMESTAMP


def token_payload_factory(
    jti: Optional[str] = None,
    sub: str = "user123",
    iat: Optional[int] = None,
    exp: Optional[int] = None,
):
    jti = jti or str(uuid.uuid4())
    iat = iat or DATETIME_NOW_TIMESTAMP
    exp = exp or int((DATETIME_NOW + datetime.timedelta(days=1)).timestamp())

    return TokenPayload(
        jti=jti,
        sub=sub,
        iat=iat,
        exp=exp,
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
    user_id = user_id or str(uuid.uuid4())
    email = email or f"user_{uuid.uuid4()}@example.com"
    created_at = created_at or DATETIME_NOW_TIMESTAMP
    hashed_password = hashed_password or hash_password("password")

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


def item_factory(
    name: Optional[str] = None,
    price: float = 1.0,
    quantity: int = 1,
    total: float = 1.0,
):
    name = name or "item1"

    return Item(
        name=name,
        price=price,
        quantity=quantity,
        total=total,
    )


def receipt_factory(
    receipt_id: Optional[str] = None,
    user_id: Optional[str] = None,
    items: Optional[list[Item]] = None,
    total: float = 0.0,
    date: Optional[int] = None,
    currency: str = Currency.EUR.value,
    market: str = Market.ALDI.value,
):
    receipt_id = receipt_id or str(uuid.uuid4())
    user_id = user_id or str(uuid.uuid4())
    items = items or [
        item_factory(),
        item_factory(name="item2", price=2.0, quantity=2, total=4.0),
    ]
    date = date or DATETIME_NOW_TIMESTAMP

    return Receipt(
        receipt_id=receipt_id,
        user_id=user_id,
        items=items,
        total=total,
        date=date,
        currency=currency,
        market=market,
    )
