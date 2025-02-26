from datetime import datetime
from typing import List, Tuple

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from smart_cart.models.receipt import Receipt
from smart_cart.schemas.receipt import ReceiptSchema
from smart_cart.utils.settings import engine


class ReceiptRepository:
    @staticmethod
    def _get_session():
        return Session(engine)

    @staticmethod
    def _get_db_receipt_by_id(session: Session, user_id: str, receipt_id: str) -> Receipt:
        statement = select(Receipt).where(Receipt.user_id == user_id, Receipt.receipt_id == receipt_id)
        db_receipt = session.exec(statement).first()
        if not db_receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")
        return db_receipt

    @staticmethod
    def _timestamp_range_for_month_year(month: int, year: int) -> Tuple[int, int]:
        start_timestamp = int(datetime(year, month, 1).timestamp())

        if month == 12:
            end_timestamp = int(datetime(year + 1, 1, 1).timestamp())
        else:
            end_timestamp = int(datetime(year, month + 1, 1).timestamp())

        return start_timestamp, end_timestamp

    @staticmethod
    def create_receipt(receipt: ReceiptSchema) -> ReceiptSchema:
        try:
            with ReceiptRepository._get_session() as session:
                db_receipt = Receipt.from_model(receipt.model_dump())
                session.add(db_receipt)
                session.commit()
                session.refresh(db_receipt)
                return ReceiptSchema(**db_receipt.model_dump())
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Duplicate receipt or constraint violation")
        except Exception:
            raise HTTPException(status_code=500, detail="Unexpected error while creating receipt")

    @staticmethod
    def get_receipt(user_id: str, receipt_id: str) -> ReceiptSchema:
        with ReceiptRepository._get_session() as session:
            return ReceiptSchema(**ReceiptRepository._get_db_receipt_by_id(session, user_id, receipt_id).model_dump())

    @staticmethod
    def get_receipts(user_id: str) -> List[ReceiptSchema]:
        with ReceiptRepository._get_session() as session:
            statement = select(Receipt).where(Receipt.user_id == user_id)
            receipts = session.exec(statement).all()
            return [ReceiptSchema(**receipt.model_dump()) for receipt in receipts]

    @staticmethod
    def get_receipts_by_month_and_year(user_id: str, month: int, year: int) -> List[ReceiptSchema]:

        start_timestamp, end_timestamp = ReceiptRepository._timestamp_range_for_month_year(month, year)

        with ReceiptRepository._get_session() as session:
            statement = select(Receipt).where(
                Receipt.user_id == user_id, Receipt.date >= start_timestamp, Receipt.date < end_timestamp
            )
            receipts = session.exec(statement).all()
            return [ReceiptSchema(**receipt.model_dump()) for receipt in receipts]

    @staticmethod
    def update_receipt(user_id: str, receipt_id: str, receipt: ReceiptSchema) -> ReceiptSchema:
        with ReceiptRepository._get_session() as session:
            db_receipt = ReceiptRepository._get_db_receipt_by_id(session, user_id, receipt_id)

            for key, value in receipt.model_dump(exclude_unset=True).items():
                setattr(db_receipt, key, value)

            session.commit()
            session.refresh(db_receipt)
            return ReceiptSchema(**db_receipt.model_dump())

    @staticmethod
    def delete_receipt(user_id: str, receipt_id: str) -> None:
        with ReceiptRepository._get_session() as session:
            db_receipt = ReceiptRepository._get_db_receipt_by_id(session, user_id, receipt_id)
            session.delete(db_receipt)
            session.commit()
