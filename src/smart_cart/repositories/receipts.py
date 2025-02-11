from typing import List, Optional

from sqlmodel import Session, select

from smart_cart.models.receipt import Receipt
from smart_cart.schemas.receipt import ReceiptSchema
from smart_cart.utils.settings import engine


class ReceiptRepository:
    @staticmethod
    def create_receipt(receipt: ReceiptSchema):
        with Session(engine) as session:
            db_receipt = Receipt.from_model(receipt.model_dump())
            session.add(db_receipt)
            session.commit()

    @staticmethod
    def get_receipt(receipt_id: str) -> Optional[ReceiptSchema]:
        with Session(engine) as session:
            db_receipt = session.get(Receipt, receipt_id)
            return ReceiptSchema(**db_receipt.model_dump()) if db_receipt else None

    @staticmethod
    def get_receipt_by_user(user_id: str) -> Optional[ReceiptSchema]:
        with Session(engine) as session:
            statement = select(Receipt).where(Receipt.user_id == user_id)
            db_receipt = session.exec(statement).first()
            return ReceiptSchema(**db_receipt.model_dump()) if db_receipt else None

    @staticmethod
    def get_receipts_by_user(user_id: str) -> List[ReceiptSchema]:
        with Session(engine) as session:
            statement = select(Receipt).where(Receipt.user_id == user_id)
            receipts = session.exec(statement).all()
            return [ReceiptSchema(**receipt.model_dump()) for receipt in receipts]

    @staticmethod
    def update_receipt(receipt: ReceiptSchema):
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
