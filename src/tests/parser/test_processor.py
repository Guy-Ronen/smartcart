import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException, UploadFile

from smart_cart.parser.processor import ReceiptProcessor
from smart_cart.schemas.response import ResponseSchema


@pytest.fixture
def mock_upload_file():
    mock = Mock(spec=UploadFile)
    mock.filename = "test_receipt.jpg"
    mock.file = Mock()
    mock.content_type = "image/jpeg"
    return mock


@pytest.fixture
def sample_response():
    results_dir = Path(__file__).parent / "results"
    with open(results_dir / "IMG1.json") as f:
        return json.load(f)


@pytest.fixture
def processor(mock_upload_file):
    return ReceiptProcessor(mock_upload_file)


@pytest.fixture
def mock_successful_process_response():
    return {
        "status": "success",
        "token": "test-token",
    }


@pytest.fixture
def mock_api_calls(mock_successful_process_response, sample_response):
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = mock_successful_process_response
        mock_post.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response
        mock_get.return_value.status_code = 200
        yield mock_post, mock_get


def test_successful_process_and_get_result(processor, mock_api_calls, sample_response):
    result = processor.process_and_get_result()

    assert isinstance(result, ResponseSchema)
    assert result.status == "done"
    assert result.success is True
    assert result.result.establishment == "REWE"
    assert result.result.total == 0.99
    assert result.result.currency == "EUR"

    mock_post, mock_get = mock_api_calls
    mock_post.assert_called_once()
    mock_get.assert_called_once()


def test_process_error_handling(processor):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "status": "error",
            "message": "Invalid receipt",
        }
        mock_post.return_value.status_code = 400

        with pytest.raises(HTTPException) as exc_info:
            processor.process_and_get_result()
        assert exc_info.value.status_code == 400


def test_result_error_handling(processor, mock_successful_process_response):
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = mock_successful_process_response
        mock_post.return_value.status_code = 200

        mock_get.return_value.json.return_value = {
            "status": "error",
            "message": "Processing failed",
        }
        mock_get.return_value.status_code = 400

        with pytest.raises(HTTPException) as exc_info:
            processor.process_and_get_result()
        assert exc_info.value.status_code == 400


def test_result_polling(processor, mock_successful_process_response, sample_response):
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = mock_successful_process_response
        mock_post.return_value.status_code = 200

        mock_get.side_effect = [
            Mock(json=lambda: {"status": "processing"}),
            Mock(json=lambda: {"status": "processing"}),
            Mock(json=lambda: sample_response),
        ]

        result = processor.process_and_get_result()

        assert isinstance(result, ResponseSchema)
        assert result.status == "done"
        assert result.success is True
        assert mock_get.call_count == 3


def test_response_schema_validation(processor, mock_api_calls):
    result = processor.process_and_get_result()

    assert isinstance(result, ResponseSchema)
    assert hasattr(result.result, "establishment")
    assert hasattr(result.result, "date")
    assert hasattr(result.result, "total")
    assert hasattr(result.result, "lineItems")
    assert hasattr(result.result, "customFields")
    assert hasattr(result.result, "addressNorm")


def test_all_result_files(processor, mock_successful_process_response):
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

            result = processor.process_and_get_result()

            assert isinstance(result, ResponseSchema)
            assert result.status == "done"
            assert result.success is True
            assert result.result.establishment is not None
            assert result.result.total is not None
            assert result.result.currency is not None


def test_unexpected_error_handling(processor):
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        with pytest.raises(HTTPException) as exc_info:
            processor.process_and_get_result()
        assert exc_info.value.status_code == 500
        assert "Invalid JSON: line 1 column 1 (char 0)" in str(exc_info.value.detail)
