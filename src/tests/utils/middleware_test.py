from contextlib import contextmanager
from unittest.mock import patch

import jwt
import pytest
from fastapi.testclient import TestClient

from smart_cart.main import app
from smart_cart.utils.factories import token_payload_factory
from smart_cart.utils.middleware import TokenMiddleware

client = TestClient(app)


@pytest.fixture
def valid_token():
    return jwt.encode(
        token_payload_factory().model_dump(),
        "local key",
        algorithm="HS256",
    )


@contextmanager
def invalid_token_header_context(token):
    with client as c:
        c.headers.update({"Authorization": f"NotBearer {token}"})
        yield c


@contextmanager
def token_header_context(token):
    with client as c:
        c.headers.update({"Authorization": f"Bearer {token}"})
        yield c


@pytest.mark.parametrize("endpoint", ["/redoc", "/openapi.json"])
def test_access_whitelisted_endpoint_without_token(endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200


def test_access_non_whitelisted_endpoint_with_invalid_token_header(valid_token):
    with invalid_token_header_context(valid_token) as c:
        response = c.get("/")
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


def test_access_non_whitelisted_endpoint_with_invalid_token():
    with token_header_context("invalid_token") as c:
        response = c.get("/")
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


def test_access_non_whitelisted_endpoint_with_valid_token_but_check_user_data_false():
    expired_token = jwt.encode(
        token_payload_factory(expires_at=0).model_dump(),
        "local key",
        algorithm="HS256",
    )

    with pytest.raises(Exception) as e:
        with token_header_context(expired_token) as c:
            c.get("/")
    assert str(e.value) == "403: Forbidden"


def test_access_non_whitelisted_endpoint_with_valid_token(valid_token):
    with token_header_context(valid_token) as c:
        response = c.get("/")
        assert response.status_code == 200