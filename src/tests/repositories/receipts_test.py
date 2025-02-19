import pytest

from smart_cart.repositories.receipts import ReceiptNotFoundError
from tests.factories.receipt import receipt_factory


def test_create_and_get_receipt(receipt_repository, user_in_db):
    expected_receipt = receipt_factory(user_id=user_in_db.user_id)
    receipt_repository.create_receipt(expected_receipt)

    actual_receipt = receipt_repository.get_user_receipt(user_in_db.user_id, expected_receipt.receipt_id)

    assert actual_receipt is not None
    assert actual_receipt.receipt_id == expected_receipt.receipt_id
    assert actual_receipt.user_id == expected_receipt.user_id
    assert actual_receipt.total == expected_receipt.total


def test_get_receipt_not_found(receipt_repository, user_in_db):
    result = receipt_repository.get_user_receipt(user_in_db.user_id, "non_existent_receipt_id")
    assert result is None


def test_get_user_receipt(receipt_repository, user_in_db):
    expected_receipt = receipt_factory(user_id=user_in_db.user_id)
    receipt_repository.create_receipt(expected_receipt)

    actual_receipt = receipt_repository.get_user_receipt(user_in_db.user_id, expected_receipt.receipt_id)

    assert actual_receipt is not None
    assert actual_receipt.receipt_id == expected_receipt.receipt_id
    assert actual_receipt.user_id == expected_receipt.user_id
    assert actual_receipt.total == expected_receipt.total


def test_get_user_receipt_not_found(receipt_repository, user_in_db):
    result = receipt_repository.get_user_receipt(user_in_db.user_id, "non_existent_receipt_id")
    assert result is None


def test_update_receipt(receipt_repository, user_in_db):
    receipt = receipt_factory(user_id=user_in_db.user_id, total=50)
    receipt_repository.create_receipt(receipt)

    receipt.total = 100
    updated_receipt = receipt_repository.update_receipt(receipt)

    assert updated_receipt.total == 100
    assert updated_receipt.receipt_id == receipt.receipt_id


def test_update_receipt_not_found(receipt_repository):
    receipt = receipt_factory(receipt_id="non_existent_receipt_id", total=100)

    with pytest.raises(ReceiptNotFoundError, match="Receipt with ID non_existent_receipt_id not found."):
        receipt_repository.update_receipt(receipt)


def test_get_receipts_by_user(receipt_repository, user_in_db):
    user_id = user_in_db.user_id
    receipt1 = receipt_factory(user_id=user_id)
    receipt2 = receipt_factory(user_id=user_id)

    receipt_repository.create_receipt(receipt1)
    receipt_repository.create_receipt(receipt2)

    receipts = receipt_repository.get_receipts_by_user(user_id)

    assert len(receipts) == 2

    receipt_ids = [r.receipt_id for r in receipts]

    assert receipt1.receipt_id in receipt_ids
    assert receipt2.receipt_id in receipt_ids


def test_get_receipts_by_user_not_found(receipt_repository):
    result = receipt_repository.get_receipts_by_user("non_existent_user_id")
    assert result == []


def test_delete_receipt(receipt_repository, user_in_db):
    receipt = receipt_factory(user_id=user_in_db.user_id)
    receipt_repository.create_receipt(receipt)

    receipt_repository.delete_receipt(receipt.receipt_id)

    result = receipt_repository.get_user_receipt(user_in_db.user_id, receipt.receipt_id)
    assert result is None


def test_delete_receipt_not_found(receipt_repository):
    with pytest.raises(ReceiptNotFoundError, match="Receipt with ID non_existent_receipt_id not found."):
        receipt_repository.delete_receipt("non_existent_receipt_id")
