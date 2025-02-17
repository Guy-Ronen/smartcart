import uuid

import pytest
from sqlmodel import Session, SQLModel

from smart_cart.repositories.receipts import Receipt, ReceiptRepository  # noqa
from smart_cart.repositories.users import User, UserRepository  # noqa
from smart_cart.utils.auth import create_access_token
from smart_cart.utils.constants import FIXED_USER_ID
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
def token():
    return create_access_token(user_factory(user_id=FIXED_USER_ID))


@pytest.fixture
def user_in_db(user_repository):
    user = user_factory(user_id=str(uuid.uuid4()))
    user_repository.create_user(user)
    return user
