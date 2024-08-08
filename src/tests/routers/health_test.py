from fastapi.testclient import TestClient

from smart_cart.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok_true_when_no_exception_occurs():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "hello": "world"}
