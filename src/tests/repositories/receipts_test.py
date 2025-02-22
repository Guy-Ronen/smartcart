import pytest
from fastapi import HTTPException

from tests.factories.receipt import receipt_factory


def test_create_and_get_receipt(receipt_repository, user_in_db):
    expected_receipt = receipt_factory(user_id=user_in_db.user_id)
    receipt_repository.create_receipt(expected_receipt)

    actual_receipt = receipt_repository.get_user_receipt(user_in_db.user_id, expected_receipt.receipt_id)

    assert actual_receipt is not None
    assert actual_receipt.receipt_id == expected_receipt.receipt_id


def test_get_receipt_not_found(receipt_repository, user_in_db):
    with pytest.raises(HTTPException) as excinfo:
        receipt_repository.get_user_receipt(user_in_db.user_id, "non_existent_receipt_id")
    assert excinfo.value.status_code == 404


def test_update_receipt(receipt_repository, user_in_db):
    receipt = receipt_factory(user_id=user_in_db.user_id, total=50)
    receipt_repository.create_receipt(receipt)

    updated_receipt = receipt_repository.update_receipt(
        user_in_db.user_id, receipt.receipt_id, receipt.model_copy(update={"total": 100})
    )

    assert updated_receipt.total == 100


def test_update_receipt_not_found(receipt_repository, user_in_db):
    with pytest.raises(HTTPException) as excinfo:
        receipt_repository.update_receipt(user_in_db.user_id, "non_existent_receipt_id", receipt_factory())
    assert excinfo.value.status_code == 404


def test_get_receipts_by_user(receipt_repository, user_in_db):
    user_id = user_in_db.user_id
    receipt1 = receipt_factory(user_id=user_id)
    receipt2 = receipt_factory(user_id=user_id)

    receipt_repository.create_receipt(receipt1)
    receipt_repository.create_receipt(receipt2)

    receipts = receipt_repository.get_receipts_by_user(user_id)

    assert len(receipts) == 2


def test_delete_receipt(receipt_repository, user_in_db):
    receipt = receipt_factory(user_id=user_in_db.user_id)
    receipt_repository.create_receipt(receipt)

    receipt_repository.delete_receipt(user_in_db.user_id, receipt.receipt_id)

    with pytest.raises(HTTPException) as excinfo:
        receipt_repository.get_user_receipt(user_in_db.user_id, receipt.receipt_id)
    assert excinfo.value.status_code == 404


def test_delete_receipt_not_found(receipt_repository):
    with pytest.raises(HTTPException) as excinfo:
        receipt_repository.delete_receipt("non_existent_user_id", "non_existent_receipt_id")
    assert excinfo.value.status_code == 404
