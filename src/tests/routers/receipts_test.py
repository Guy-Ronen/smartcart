from unittest.mock import patch

import pytest
from fastapi import HTTPException

from smart_cart.factories.receipt import receipt_factory


@pytest.fixture
def receipt():
    return receipt_factory()


def test_failed_receipt_creation_should_return_400(client, receipt, token):
    with patch("smart_cart.repositories.receipts.ReceiptRepository.create_receipt") as mock_create:
        mock_create.side_effect = HTTPException(status_code=400, detail="Failed to create receipt")

        response = client.post(
            "/api/v1/receipts",
            json=receipt.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 400
        assert response.json() == {"detail": "Failed to create receipt"}


def test_signup_should_return_201(client, token):
    receipt = receipt_factory()
    payload = receipt.model_dump()

    response = client.post(
        "/api/v1/receipts",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 201
    assert response.json() == payload
