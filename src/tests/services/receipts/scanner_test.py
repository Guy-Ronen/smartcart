import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from smart_cart.schemas.receipt import ReceiptSchema
from smart_cart.services.receipts.scanner import ReceiptScanner


@pytest.fixture
def scanner(mock_upload_file):
    return ReceiptScanner(mock_upload_file)


@pytest.fixture
def mock_api_calls(mock_successful_process_response, sample_response):
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = mock_successful_process_response
        mock_post.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response
        mock_get.return_value.status_code = 200
        yield mock_post, mock_get


def test_successful_process_and_get_result(scanner, mock_api_calls):
    result = scanner.process_and_get_result()

    assert isinstance(result, ReceiptSchema)
    assert result.market == "REWE"
    assert result.total == 0.99
    assert result.currency == "EUR"
    assert result.items[0].name == "SUPPENGRUEN"

    mock_post, mock_get = mock_api_calls
    mock_post.assert_called_once()
    mock_get.assert_called_once()


def test_process_error_handling(scanner):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "status": "error",
            "message": "Invalid receipt",
        }
        mock_post.return_value.status_code = 400

        with pytest.raises(HTTPException) as exc_info:
            scanner.process_and_get_result()
        assert exc_info.value.status_code == 400


def test_result_error_handling(scanner, mock_successful_process_response):
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = mock_successful_process_response
        mock_post.return_value.status_code = 200

        mock_get.return_value.json.return_value = {
            "status": "error",
            "message": "Processing failed",
        }
        mock_get.return_value.status_code = 400

        with pytest.raises(HTTPException) as exc_info:
            scanner.process_and_get_result()
        assert exc_info.value.status_code == 400


def test_result_polling(scanner, mock_successful_process_response, sample_response):
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = mock_successful_process_response
        mock_post.return_value.status_code = 200

        mock_get.side_effect = [
            Mock(json=lambda: {"status": "processing"}),
            Mock(json=lambda: {"status": "processing"}),
            Mock(json=lambda: sample_response),
        ]

        result = scanner.process_and_get_result()

        assert isinstance(result, ReceiptSchema)
        assert result.market == "REWE"
        assert result.total == 0.99
        assert result.items[0].name == "SUPPENGRUEN"
        assert mock_get.call_count == 3


def test_response_schema_validation(scanner, mock_api_calls):
    result = scanner.process_and_get_result()

    assert isinstance(result, ReceiptSchema)
    assert result.market == "REWE"
    assert result.total > 0
    assert result.items


def test_all_result_files(scanner, mock_successful_process_response):
    results_dir = Path(__file__).parent / "results"
    result_files = [
        "IMG1.json",
        "IMG2.json",
        "IMG3.json",
        "IMG4.json",
        "IMG5.json",
        "IMG6.json",
    ]

    for result_file in result_files:
        with open(results_dir / result_file) as f:
            sample_response = json.load(f)

        with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
            mock_post.return_value.json.return_value = mock_successful_process_response
            mock_post.return_value.status_code = 200

            mock_get.return_value.json.return_value = sample_response
            mock_get.return_value.status_code = 200

            result = scanner.process_and_get_result()
            assert isinstance(result, ReceiptSchema)
            assert result.total > 0
            assert result.items


def test_unexpected_error_handling(scanner):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        with pytest.raises(HTTPException) as exc_info:
            scanner.process_and_get_result()
        assert exc_info.value.status_code == 500
        assert "Invalid JSON" in str(exc_info.value.detail)
