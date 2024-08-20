import boto3
import pytest
from moto import mock_aws

from smart_cart.repositories.users import UserRepository
from smart_cart.utils.settings import settings


@pytest.fixture(autouse=True, scope="session")
def automock():
    with mock_aws():
        yield


@pytest.fixture(autouse=True, scope="session")
def dynamodb_users_table():
    dynamodb = boto3.client("dynamodb", region_name=settings.region)
    dynamodb.create_table(
        TableName=settings.table_name,
        KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "user_id", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )


@pytest.fixture
def user_repository():
    return UserRepository(
        table_name=settings.table_name,
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
