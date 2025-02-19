from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

from smart_cart.schemas.receipt import Category, Currency, Market

if TYPE_CHECKING:
    from smart_cart.models.user import User


class Item(SQLModel):
    name: str
    price: float
    quantity: int
    total: float
    category: Category


class Receipt(SQLModel, table=True):  # type: ignore
    receipt_id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.user_id", index=True)
    items: Optional[List[Item]] = Field(default=None, sa_column=Column(JSON))
    total: float
    date: int = Field(index=True)
    currency: Currency
    market: Market = Field(index=True)

    user: Optional["User"] = Relationship(back_populates="receipts")

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
