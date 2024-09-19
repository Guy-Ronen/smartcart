import uuid

from smart_cart.factories.receipt import receipt_factory


def test_create_and_get_receipt(receipt_repository):

    expected_receipt = receipt_factory(receipt_id="123")

    receipt_repository.create_receipt(expected_receipt)

    actual_receipt = receipt_repository.get_receipt(expected_receipt.receipt_id)

    assert actual_receipt == expected_receipt


def test_get_receipt_not_found(receipt_repository):
    result = receipt_repository.get_receipt("non_existent_receipt_id")

    assert result is None


def test_get_receipt_by_user(receipt_repository):

    user_id = str(uuid.uuid4())

    expected_receipt = receipt_factory(user_id=user_id)

    receipt_repository.create_receipt(expected_receipt)

    actual_receipt = receipt_repository.get_receipt_by_user(expected_receipt.user_id)

    assert actual_receipt == expected_receipt


def test_get_receipt_by_user_not_found(receipt_repository):
    result = receipt_repository.get_receipt_by_user("non_existent_user_id")
    assert result is None


def test_update_receipt(receipt_repository):
    receipt = receipt_factory(total=50)
    receipt_repository.create_receipt(receipt)

    receipt.total = 100

    receipt_repository.update_receipt(receipt)

    updated_receipt = receipt_repository.get_receipt(receipt.receipt_id)

    assert updated_receipt.total == 100


def test_get_receipts_by_user(receipt_repository):
    user_id = str(uuid.uuid4())

    receipt1 = receipt_factory(user_id=user_id)
    receipt2 = receipt_factory(user_id=user_id)

    receipt_repository.create_receipt(receipt1)
    receipt_repository.create_receipt(receipt2)

    receipts = receipt_repository.get_receipts_by_user(user_id)

    assert len(receipts) == 2
    assert receipt1 in receipts
    assert receipt2 in receipts


def test_get_receipts_by_user_not_found(receipt_repository):
    result = receipt_repository.get_receipts_by_user("non_existent_user_id")
    assert result == []
