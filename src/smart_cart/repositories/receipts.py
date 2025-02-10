from typing import List, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, Session, SQLModel, select

from smart_cart.database import engine
from smart_cart.models.receipt import Category, Currency, Market
from smart_cart.models.receipt import Receipt as ReceiptModel


class Item(SQLModel):
    name: str
    price: float
    quantity: int
    total: float
    category: Category


class Receipt(SQLModel, table=True): # type: ignore
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


class ReceiptRepository:
    @staticmethod
    def create_receipt(receipt: ReceiptModel):
        with Session(engine) as session:
            db_receipt = Receipt.from_model(receipt.model_dump())
            session.add(db_receipt)
            session.commit()

    @staticmethod
    def get_receipt(receipt_id: str) -> Optional[ReceiptModel]:
        with Session(engine) as session:
            db_receipt = session.get(Receipt, receipt_id)
            return ReceiptModel(**db_receipt.model_dump()) if db_receipt else None

    @staticmethod
    def get_receipt_by_user(user_id: str) -> Optional[ReceiptModel]:
        with Session(engine) as session:
            statement = select(Receipt).where(Receipt.user_id == user_id)
            db_receipt = session.exec(statement).first()
            return ReceiptModel(**db_receipt.model_dump()) if db_receipt else None

    @staticmethod
    def get_receipts_by_user(user_id: str) -> List[ReceiptModel]:
        with Session(engine) as session:
            statement = select(Receipt).where(Receipt.user_id == user_id)
            receipts = session.exec(statement).all()
            return [ReceiptModel(**receipt.model_dump()) for receipt in receipts]

    @staticmethod
    def update_receipt(receipt: ReceiptModel):
        with Session(engine) as session:
            db_receipt = session.get(Receipt, receipt.receipt_id)
            if db_receipt:
                for key, value in receipt.model_dump().items():
                    setattr(db_receipt, key, value)
                session.commit()

    @staticmethod
    def delete_receipt(receipt_id: str):
        with Session(engine) as session:
            db_receipt = session.get(Receipt, receipt_id)
            if db_receipt:
                session.delete(db_receipt)
                session.commit()
