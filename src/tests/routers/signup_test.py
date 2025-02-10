import jwt

from smart_cart.factories.user import user_factory, user_signup_factory
from smart_cart.schemas.token import TokenPayload
from smart_cart.utils.settings import settings


def test_existing_user_should_return_400(client, user_repository):
    user = user_factory(email="john.doe@example.com")
    user_repository.create_user(user)

    user_sign_up = user_signup_factory(email="john.doe@example.com")

    response = client.post("/api/v1/signup", json=user_sign_up.model_dump())

    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_signup_should_return_201(client):
    user_sign_up = user_signup_factory()

    response = client.post("/api/v1/signup", json=user_sign_up.model_dump())

    assert response.status_code == 201
    assert "access_token" in response.json()
    assert "user" in response.json()

    token_payload = TokenPayload(
        **jwt.decode(
            response.json()["access_token"], settings.token_payload_secret_key, algorithms=[settings.hashing_algorithm]
        )
    )

    assert token_payload.sub
    assert token_payload.iat
    assert token_payload.exp
    assert token_payload.exp > token_payload.iat

    assert response.json()["user"]["user_id"]
    assert response.json()["user"]["email"] == user_sign_up.email
    assert response.json()["user"]["first_name"] == user_sign_up.first_name
    assert response.json()["user"]["last_name"] == user_sign_up.last_name
    assert response.json()["user"]["is_active"]
