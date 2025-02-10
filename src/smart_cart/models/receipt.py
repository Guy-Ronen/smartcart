from typing import List, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from smart_cart.schemas.receipt import Category, Currency, Market


class Item(SQLModel):
    name: str
    price: float
    quantity: int
    total: float
    category: Category


class Receipt(SQLModel, table=True):  # type: ignore
    receipt_id: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    items: Optional[List[Item]] = Field(default=None, sa_column=Column(JSON))
    total: float
    date: int = Field(index=True)
    currency: Currency
    market: Market = Field(index=True)

    @classmethod
    def from_model(cls, data: dict) -> "Receipt":
        return cls(
            receipt_id=data["receipt_id"],
            user_id=data["user_id"],
            items=[item for item in data.get("items", [])],
            total=data["total"],
            date=data["date"],
            currency=Currency(data["currency"]),
            market=Market(data["market"]),
        )
