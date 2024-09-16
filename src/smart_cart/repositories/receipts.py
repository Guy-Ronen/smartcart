from typing import List

from pydantic import BaseModel
from pynamodb.attributes import (
    ListAttribute,
    MapAttribute,
    NumberAttribute,
    UnicodeAttribute,
)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model

from smart_cart.models.receipt import Receipt as ReceiptModel
from smart_cart.utils.settings import settings


class Item(MapAttribute):
    name = UnicodeAttribute()
    price = NumberAttribute()
    quantity = NumberAttribute()
    total = NumberAttribute()


class UserIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "user_id-index"
        projection = AllProjection()
        read_capacity_units = 1
        write_capacity_units = 1

    user_id = UnicodeAttribute(hash_key=True)


class Receipt(Model):
    class Meta:
        table_name = settings.receipts_table_name
        region = settings.region
        aws_access_key_id = settings.aws_access_key_id
        aws_secret_access_key = settings.aws_secret_access_key
        aws_session_token = settings.aws_session_token
        host = settings.host

    receipt_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute()
    user_index = UserIndex()
    items = ListAttribute(of=Item)
    total = NumberAttribute()
    date = NumberAttribute()
    currency = UnicodeAttribute()
    market = UnicodeAttribute()

    @classmethod
    def from_entity(cls, model: ReceiptModel):
        return cls(
            receipt_id=model.receipt_id,
            user_id=model.user_id,
            items=[Item(**item.model_dump()) for item in model.items],
            total=model.total,
            date=model.date,
            currency=model.currency.value,
            market=model.market.value,
        )


class ReceiptRepository(BaseModel):
    table_name: str
    region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    host: str

    @staticmethod
    def create_receipt(receipt: ReceiptModel):
        item = Receipt.from_entity(receipt)
        item.save()

    @staticmethod
    def get_receipt(receipt_id: str) -> ReceiptModel | None:
        try:
            item = Receipt.get(receipt_id)
        except Receipt.DoesNotExist:
            return None
        return ReceiptModel.from_dynamoItem(item.to_simple_dict())

    @staticmethod
    def get_receipt_by_user(user_id: str) -> list[ReceiptModel]:
        try:
            result = Receipt.user_index.query(user_id)
            item = next(result)
        except StopIteration:
            return None
        return ReceiptModel.from_dynamoItem(item.to_simple_dict())

    @staticmethod
    def update_receipt(receipt: ReceiptModel):
        item = Receipt.from_entity(receipt)
        item.save()

    @staticmethod
    def get_receipts_by_user(user_id: str) -> List[ReceiptModel]:
        result = Receipt.user_index.query(user_id)
        receipts = [ReceiptModel.from_dynamoItem(item.to_simple_dict()) for item in result]
        if not receipts:
            return []

        return receipts
