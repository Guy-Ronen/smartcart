import uuid
from unittest.mock import patch

import pytest
from sqlalchemy.exc import IntegrityError

from tests.factories.receipt import receipt_factory


@pytest.fixture
def receipt():
    return receipt_factory()


def test_failed_receipt_creation_should_return_400(client, receipt, token):
    with patch("smart_cart.repositories.receipts.Session.commit", side_effect=IntegrityError("", "", "")):
        response = client.post(
            "/api/v1/receipts",
            json=receipt.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Duplicate receipt or constraint violation"}


def test_failed_receipt_creation_should_return_500(client, receipt, token):
    with patch("smart_cart.repositories.receipts.Session.commit", side_effect=Exception()):
        response = client.post(
            "/api/v1/receipts",
            json=receipt.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 500
    assert response.json() == {"detail": "Unexpected error while creating receipt"}


def test_successful_receipt_creation_should_return_201(client, receipt, token, user_in_db):
    receipt = receipt_factory(user_id=user_in_db.user_id)
    payload = receipt.model_dump()

    response = client.post(
        "/api/v1/receipts",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert response.json()["receipt_id"] == receipt.receipt_id


def test_get_existing_receipt_should_return_200(client, token, user_in_db, receipt_repository):
    receipt = receipt_factory(user_id=user_in_db.user_id)
    receipt_repository.create_receipt(receipt)

    response = client.get(
        f"/api/v1/receipts/{receipt.receipt_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["receipt_id"] == receipt.receipt_id


def test_get_nonexistent_receipt_should_return_404(client, token):
    response = client.get(
        "/api/v1/receipts/nonexistent-receipt",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}


def test_get_all_receipts_should_return_list(client, token, user_in_db, receipt_repository):
    receipt1 = receipt_factory(user_id=user_in_db.user_id)
    receipt2 = receipt_factory(user_id=user_in_db.user_id)

    receipt_repository.create_receipt(receipt1)
    receipt_repository.create_receipt(receipt2)

    response = client.get("/api/v1/receipts", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_existing_receipt_should_return_200(client, token, user_in_db, receipt_repository):
    receipt = receipt_factory(user_id=user_in_db.user_id, total=50.0)
    receipt_repository.create_receipt(receipt)

    updated_data = receipt.model_dump()
    updated_data["total"] = 100.0

    response = client.put(
        f"/api/v1/receipts/{receipt.receipt_id}",
        json=updated_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 100.0


def test_update_nonexistent_receipt_should_return_404(client, token, user_in_db):
    non_existent_receipt_id = str(uuid.uuid4())

    updated_data = receipt_factory(user_id=user_in_db.user_id).model_dump()
    updated_data["total"] = 100.0

    response = client.put(
        f"/api/v1/receipts/{non_existent_receipt_id}",
        json=updated_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}


def test_delete_existing_receipt_should_return_204(client, token, user_in_db, receipt_repository):
    receipt = receipt_factory(user_id=user_in_db.user_id)
    receipt_repository.create_receipt(receipt)

    response = client.delete(
        f"/api/v1/receipts/{receipt.receipt_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/receipts/{receipt.receipt_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 404


def test_delete_nonexistent_receipt_should_return_404(client, token):
    non_existent_receipt_id = str(uuid.uuid4())

    response = client.delete(
        f"/api/v1/receipts/{non_existent_receipt_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}
