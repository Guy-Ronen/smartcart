from unittest.mock import patch

import pytest

from tests.factories.receipt import receipt_factory


@pytest.fixture
def receipt():
    return receipt_factory()


def test_failed_receipt_creation_should_return_400(client, receipt, token):
    with patch("smart_cart.repositories.receipts.Session.commit", side_effect=Exception("DB error")):
        response = client.post(
            "/api/v1/receipts",
            json=receipt.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to create receipt"}


def test_successful_receipt_creation_should_return_201(client, receipt, token, user_in_db):
    receipt = receipt_factory(user_id=user_in_db.user_id)
    payload = receipt.model_dump()

    response = client.post(
        "/api/v1/receipts",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert response.json() == payload
