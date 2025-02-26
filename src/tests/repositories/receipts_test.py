import datetime

import pytest
from fastapi import HTTPException

from tests.factories.receipt import receipt_factory


def test_create_and_get_receipt(receipt_repository, user_in_db):
    expected_receipt = receipt_factory(user_id=user_in_db.user_id)
    receipt_repository.create_receipt(expected_receipt)

    actual_receipt = receipt_repository.get_receipt(user_in_db.user_id, expected_receipt.receipt_id)

    assert actual_receipt is not None
    assert actual_receipt.receipt_id == expected_receipt.receipt_id


def test_get_receipt_not_found(receipt_repository, user_in_db):
    with pytest.raises(HTTPException) as excinfo:
        receipt_repository.get_receipt(user_in_db.user_id, "non_existent_receipt_id")
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


def test_get_receipts(receipt_repository, user_in_db):
    user_id = user_in_db.user_id
    receipt1 = receipt_factory(user_id=user_id)
    receipt2 = receipt_factory(user_id=user_id)

    receipt_repository.create_receipt(receipt1)
    receipt_repository.create_receipt(receipt2)

    receipts = receipt_repository.get_receipts(user_id)

    assert len(receipts) == 2


def test_get_receipts_by_month_and_year(receipt_repository, user_in_db):
    now = datetime.datetime.now()
    one_day_ago = now - datetime.timedelta(days=1)
    last_month_date = now - datetime.timedelta(days=45)

    receipt1 = receipt_factory(user_id=user_in_db.user_id, date=int(one_day_ago.timestamp()))
    receipt2 = receipt_factory(user_id=user_in_db.user_id, date=int(last_month_date.timestamp()))

    receipt_repository.create_receipt(receipt1)
    receipt_repository.create_receipt(receipt2)

    month = now.month
    year = now.year

    last_month = now.month - 1
    if last_month == 0:
        last_month = 12

    receipts = receipt_repository.get_receipts_by_month_and_year(user_in_db.user_id, month, year)
    assert len(receipts) == 1
    assert receipts[0].receipt_id == receipt1.receipt_id

    receipts = receipt_repository.get_receipts_by_month_and_year(user_in_db.user_id, last_month, year)
    assert len(receipts) == 1
    assert receipts[0].receipt_id == receipt2.receipt_id


def test_get_receipts_by_month_and_year_handles_next_year(receipt_repository, user_in_db):
    this_year = datetime.datetime.now().year
    next_year = this_year + 1
    december_month = 12

    receipt = receipt_factory(
        user_id=user_in_db.user_id, date=int(datetime.datetime(next_year, december_month, 15).timestamp())
    )
    receipt_repository.create_receipt(receipt)

    receipts = receipt_repository.get_receipts_by_month_and_year(user_in_db.user_id, december_month, next_year)

    assert len(receipts) == 1
    assert receipts[0].receipt_id == receipt.receipt_id


def test_get_receipts_does_not_include_next_month(receipt_repository, user_in_db):
    now = datetime.datetime.now()
    current_month = now.month
    next_month = current_month + 1 if current_month < 12 else 1
    year = now.year

    receipt_in_next_month = receipt_factory(
        user_id=user_in_db.user_id, date=int(datetime.datetime(year, next_month, 1).timestamp())
    )
    receipt_repository.create_receipt(receipt_in_next_month)

    receipts = receipt_repository.get_receipts_by_month_and_year(user_in_db.user_id, current_month, year)
    assert len(receipts) == 0


def test_get_receipts_returns_empty_list_when_no_receipts_exist(receipt_repository, user_in_db):
    now = datetime.datetime.now()
    month = now.month
    year = now.year

    receipts = receipt_repository.get_receipts_by_month_and_year(user_in_db.user_id, month, year)
    assert receipts == []


def test_delete_receipt(receipt_repository, user_in_db):
    receipt = receipt_factory(user_id=user_in_db.user_id)
    receipt_repository.create_receipt(receipt)

    receipt_repository.delete_receipt(user_in_db.user_id, receipt.receipt_id)

    with pytest.raises(HTTPException) as excinfo:
        receipt_repository.get_receipt(user_in_db.user_id, receipt.receipt_id)
    assert excinfo.value.status_code == 404


def test_delete_receipt_not_found(receipt_repository):
    with pytest.raises(HTTPException) as excinfo:
        receipt_repository.delete_receipt("non_existent_user_id", "non_existent_receipt_id")
    assert excinfo.value.status_code == 404
