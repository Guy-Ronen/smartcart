from typing import List, Optional

from sqlmodel import Session, select

from smart_cart.models.receipt import Receipt
from smart_cart.schemas.receipt import ReceiptSchema
from smart_cart.utils.settings import engine


class ReceiptNotFoundError(Exception):
    pass


class ReceiptRepository:
    @staticmethod
    def _get_session():
        return Session(engine)

    @staticmethod
    def _get_db_receipt_by_id(session: Session, receipt_id: str) -> Optional[Receipt]:
        return session.get(Receipt, receipt_id)

    @staticmethod
    def create_receipt(receipt: ReceiptSchema) -> ReceiptSchema:
        with ReceiptRepository._get_session() as session:
            db_receipt = Receipt.from_model(receipt.model_dump())
            session.add(db_receipt)
            session.commit()
            session.refresh(db_receipt)
            return ReceiptSchema(**db_receipt.model_dump())

    @staticmethod
    def get_receipt(receipt_id: str) -> Optional[ReceiptSchema]:
        with ReceiptRepository._get_session() as session:
            db_receipt = ReceiptRepository._get_db_receipt_by_id(session, receipt_id)
            return ReceiptSchema(**db_receipt.model_dump()) if db_receipt else None

    @staticmethod
    def get_receipt_by_user(user_id: str) -> Optional[ReceiptSchema]:
        with ReceiptRepository._get_session() as session:
            statement = select(Receipt).where(Receipt.user_id == user_id)
            db_receipt = session.exec(statement).first()
            return ReceiptSchema(**db_receipt.model_dump()) if db_receipt else None

    @staticmethod
    def get_receipts_by_user(user_id: str) -> List[ReceiptSchema]:
        with ReceiptRepository._get_session() as session:
            statement = select(Receipt).where(Receipt.user_id == user_id)
            receipts = session.exec(statement).all()
            return [ReceiptSchema(**receipt.model_dump()) for receipt in receipts]

    @staticmethod
    def update_receipt(receipt: ReceiptSchema) -> ReceiptSchema:
        with ReceiptRepository._get_session() as session:
            db_receipt = ReceiptRepository._get_db_receipt_by_id(session, receipt.receipt_id)
            if not db_receipt:
                raise ReceiptNotFoundError(f"Receipt with ID {receipt.receipt_id} not found.")

            for key, value in receipt.model_dump().items():
                setattr(db_receipt, key, value)

            session.commit()
            session.refresh(db_receipt)
            return ReceiptSchema(**db_receipt.model_dump())

    @staticmethod
    def delete_receipt(receipt_id: str) -> None:
        with ReceiptRepository._get_session() as session:
            db_receipt = ReceiptRepository._get_db_receipt_by_id(session, receipt_id)
            if not db_receipt:
                raise ReceiptNotFoundError(f"Receipt with ID {receipt_id} not found.")

            session.delete(db_receipt)
            session.commit()
