import io
import json
import uuid
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi import UploadFile
from sqlmodel import Session, SQLModel

from smart_cart.repositories.receipts import Receipt, ReceiptRepository  # noqa
from smart_cart.repositories.users import User, UserRepository  # noqa
from smart_cart.utils.auth import create_access_token
from smart_cart.utils.settings import engine
from tests.factories.user import user_factory


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session


@pytest.fixture
def user_repository():
    return UserRepository()


@pytest.fixture
def receipt_repository():
    return ReceiptRepository()


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from smart_cart.main import app

    return TestClient(app)


@pytest.fixture
def user_in_db(user_repository):
    user = user_factory(user_id=str(uuid.uuid4()))
    user_repository.create_user(user)
    return user


@pytest.fixture
def token(user_in_db):
    return create_access_token(user_factory(user_id=user_in_db.user_id))


@pytest.fixture
def mock_upload_file():
    file_content = b"fake image data"
    file_stream = io.BytesIO(file_content)
    upload_file = Mock(spec=UploadFile)
    upload_file.filename = "test_receipt.jpg"
    upload_file.file = file_stream
    upload_file.content_type = "image/jpeg"
    return upload_file


@pytest.fixture
def sample_response():
    results_dir = Path(__file__).parent / "parser" / "receipts"
    with open(results_dir / "IMG1.json") as f:
        return json.load(f)


@pytest.fixture
def mock_successful_process_response():
    return {
        "status": "success",
        "token": "test-token",
    }
