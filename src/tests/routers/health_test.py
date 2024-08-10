from unittest.mock import patch

from fastapi.testclient import TestClient

from smart_cart.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok_true_when_no_exception_occurs():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "hello": "world"}


@patch("smart_cart.routers.health.perform_health_check", side_effect=Exception("Something went wrong"))
def test_health_endpoint_returns_ok_false_when_exception_occurs(mock_health_check):
    response = client.get("/health")

    assert response.status_code == 500
    assert response.json() == {"ok": False, "error": "Something went wrong"}
