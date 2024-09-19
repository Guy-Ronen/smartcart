import datetime
import uuid
from typing import Optional

from smart_cart.models.receipt import Category, Currency, Item, Market, Receipt
from smart_cart.models.token import TokenPayload
from smart_cart.models.user import User, UserLogin, UserSignUp
from smart_cart.utils.auth import hash_password
from smart_cart.utils.constants import DATETIME_NOW, DATETIME_NOW_TIMESTAMP


def item_factory(
    name: Optional[str] = None,
    price: float = 1.0,
    quantity: int = 1,
    total: float = 1.0,
    category: str = Category.OTHER.value,
):
    name = name or "item1"

    return Item(
        name=name,
        price=price,
        quantity=quantity,
        total=total,
        category=category,
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
        item_factory(name="item2", price=2.0, quantity=2, total=4.0, category=Category.DRINKS.value),
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
