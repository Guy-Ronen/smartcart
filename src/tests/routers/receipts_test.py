import datetime
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


def test_get_receipts_for_current_month(client, token, user_in_db, receipt_repository):
    now = datetime.datetime.now()
    this_month = now.month
    this_year = now.year

    one_day_ago = now - datetime.timedelta(days=1)
    if one_day_ago.month != this_month:
        one_day_ago = now

    receipt = receipt_factory(user_id=user_in_db.user_id, date=int(now.timestamp()))
    receipt1 = receipt_factory(user_id=user_in_db.user_id, date=int(one_day_ago.timestamp()))

    receipt_repository.create_receipt(receipt)
    receipt_repository.create_receipt(receipt1)

    response = client.get(
        f"/api/v1/receipts?month={this_month}&year={this_year}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert {r["receipt_id"] for r in response.json()} == {receipt.receipt_id, receipt1.receipt_id}


def test_get_receipts_for_last_month(client, token, user_in_db, receipt_repository):
    now = datetime.datetime.now(datetime.timezone.utc)

    first_of_current_month = datetime.datetime(now.year, now.month, 1)
    last_month_date = first_of_current_month - datetime.timedelta(days=1)

    last_month = now.month - 1 if now.month > 1 else 12
    last_month_year = now.year if now.month > 1 else now.year - 1

    receipt2 = receipt_factory(user_id=user_in_db.user_id, date=int(last_month_date.timestamp()))
    receipt_repository.create_receipt(receipt2)

    response = client.get(
        f"/api/v1/receipts?month={last_month}&year={last_month_year}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["receipt_id"] == receipt2.receipt_id


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


def test_process_receipt_success(client, mock_upload_file, sample_response, mock_successful_process_response, token):
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = mock_successful_process_response
        mock_post.return_value.status_code = 200

        mock_get.return_value.json.return_value = sample_response
        mock_get.return_value.status_code = 200

        response = client.post(
            "/api/v1/process_receipt",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (mock_upload_file.filename, mock_upload_file.file, mock_upload_file.content_type)},
        )

        assert response.status_code == 200

        data = response.json()

        assert "receipt_id" in data
        assert data["market"] == "REWE"
        assert data["total"] == 0.99
        assert data["currency"] == "EUR"
        assert data["items"][0]["name"] == "SUPPENGRUEN"


def test_process_receipt_known_api_error(client, mock_upload_file, token):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"status": "error", "message": "Invalid receipt"}
        mock_post.return_value.status_code = 400

        response = client.post(
            "/api/v1/process_receipt",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (mock_upload_file.filename, mock_upload_file.file, mock_upload_file.content_type)},
        )

        assert response.status_code == 400
        assert "Error processing receipt" in response.json()["detail"]


def test_process_receipt_unexpected_error(client, mock_upload_file, token):
    with patch("requests.post") as mock_post:
        mock_post.side_effect = Exception("Something went wrong")

        response = client.post(
            "/api/v1/process_receipt",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (mock_upload_file.filename, mock_upload_file.file, mock_upload_file.content_type)},
        )

        assert response.status_code == 500
        assert "Something went wrong" in response.json()["detail"]
