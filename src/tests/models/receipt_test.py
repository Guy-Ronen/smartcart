import uuid

import pytest
from pydantic import ValidationError

from smart_cart.models.receipt import Currency, Item, Market, Receipt
from smart_cart.utils.factories import item_factory, receipt_factory

# Item #


def test_item():
    item = item_factory().model_dump()

    item_schema = Item(**item)

    assert item_schema.name == item["name"]
    assert item_schema.price == item["price"]
    assert item_schema.quantity == item["quantity"]
    assert item_schema.total == item["total"]

    assert item_schema.model_dump() == item


def test_receipt():
    receipt = receipt_factory().model_dump()

    receipt_schema = Receipt(**receipt)

    assert receipt_schema.receipt_id == receipt["receipt_id"]
    assert receipt_schema.user_id == receipt["user_id"]
    assert receipt_schema.items == [Item(**item) for item in receipt["items"]]
    assert receipt_schema.total == receipt["total"]
    assert receipt_schema.date == receipt["date"]
    assert receipt_schema.currency == Currency(receipt["currency"])
    assert receipt_schema.market == Market(receipt["market"])

    assert uuid.UUID(receipt_schema.receipt_id)
    assert uuid.UUID(receipt_schema.user_id)

    assert receipt_schema.model_dump() == receipt


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("receipt_id", 123),
        ("user_id", 123),
        ("items", [123]),
        ("total", "invalid_total"),
        ("date", "invalid_date"),
        ("currency", "invalid_currency"),
        ("market", "invalid_market"),
    ],
)
def test_create_receipt_invalid(field, invalid_value):
    with pytest.raises(ValidationError):
        Receipt(**{field: invalid_value})


def test_from_dynamodb_item(receipt_repository):
    expected_receipt = receipt_factory()

    receipt_repository.create_receipt(expected_receipt)

    item = receipt_repository.get_receipt(expected_receipt.receipt_id).model_dump()

    actual_receipt = Receipt.from_dynamoItem(item)

    assert actual_receipt == expected_receipt
