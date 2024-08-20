import jwt

from smart_cart.models.token import TokenPayload
from smart_cart.utils.auth import verify_password
from smart_cart.utils.factories import user_factory
from smart_cart.utils.settings import settings


def test_existing_user_should_return_400(client, user_repository):
    user = user_factory()
    user_repository.create_user(user)

    response = client.post("/api/v1/signup", json=user.model_dump())

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already exists"}


def test_signup_should_return_201(client):
    user = user_factory()

    response = client.post("/api/v1/signup", json=user.model_dump())

    assert response.status_code == 201

    assert response.json()["user"]["email"] == user.email
    assert response.json()["user"]["username"] == user.username
    assert response.json()["user"]["first_name"] == user.first_name
    assert response.json()["user"]["last_name"] == user.last_name
    assert response.json()["user"]["is_active"] == user.is_active
    assert response.json()["user"]["is_superuser"] == user.is_superuser
    assert response.json()["user"]["is_staff"] == user.is_staff
    assert response.json()["user"]["created_at"] == user.created_at
    assert response.json()["user"]["updated_at"] is None
    assert response.json()["user"]["last_login"] is None
    assert response.json()["user"]["user_id"] is not None

    assert verify_password(user.hashed_password, response.json()["user"]["hashed_password"])

    assert TokenPayload(
        **jwt.decode(response.json()["access_token"], settings.token_payload_secret_key, algorithms=["HS256"])
    )
