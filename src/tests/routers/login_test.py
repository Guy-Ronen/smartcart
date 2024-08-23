from smart_cart.utils.auth import hash_password
from smart_cart.utils.factories import user_factory, user_login_factory


def test_user_email_not_found_should_return_404(client):
    user_login = user_login_factory()

    response = client.post("/api/v1/login", json=user_login.model_dump())

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_user_incorrect_password_should_return_401(client, user_repository):
    user = user_factory()
    user_repository.create_user(user)

    user_login = user_login_factory(email=user.email, password="wrong_password")

    response = client.post("/api/v1/login", json=user_login.model_dump())

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}


def test_user_login_should_return_access_token(client, user_repository):
    plain_password = "password"
    user = user_factory(hashed_password=hash_password(plain_password))
    user_repository.create_user(user)

    user_login = user_login_factory(email=user.email, password=plain_password)

    response = client.post("/api/v1/login", json=user_login.model_dump())

    assert response.status_code == 200
