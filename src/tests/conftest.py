import pytest

from smart_cart.repositories.receipts import ReceiptRepository
from smart_cart.repositories.users import UserRepository
from smart_cart.utils.settings import settings


@pytest.fixture
def user_repository():
    return UserRepository(
        table_name=settings.users_table_name,
        region=settings.region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        aws_session_token=settings.aws_session_token,
        host=settings.host,
    )


@pytest.fixture
def receipt_repository():
    return ReceiptRepository(
        table_name=settings.receipts_table_name,
        region=settings.region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        aws_session_token=settings.aws_session_token,
        host=settings.host,
    )


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from smart_cart.main import app

    return TestClient(app)
