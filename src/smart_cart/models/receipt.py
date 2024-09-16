import enum
import uuid
from typing import List

from pydantic import BaseModel


class Currency(enum.Enum):
    EUR = "EUR"


class Market(enum.Enum):
    ALDI = "ALDI"
    LIDL = "LIDL"
    NETTO = "NETTO"
    REWE = "REWE"
    EDEKA = "EDEKA"
    KAUFLAND = "KAUFLAND"
    PENNY = "PENNY"
    REAL = "REAL"

class Item(BaseModel):
    name: str
    price: float
    quantity: int
    total: float


class Receipt(BaseModel):
    receipt_id: str = str(uuid.uuid4())
    user_id: str
    items: List[Item]
    total: float
    date: int
    currency: Currency
    market: Market

    @classmethod
    def from_dynamoItem(cls, item: dict) -> "Receipt":
        return cls(
            receipt_id=item["receipt_id"],
            user_id=item["user_id"],
            items=[Item(**item_data) for item_data in item["items"]],
            total=item["total"],
            date=item["date"],
            currency=Currency(item["currency"]),
            market=Market(item["market"]),
        )