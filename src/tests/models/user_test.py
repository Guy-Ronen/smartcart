import uuid

import pytest
from pydantic import ValidationError

from smart_cart.factories.user import (
    user_factory,
    user_login_factory,
    user_signup_factory,
)
from smart_cart.models.user import User, UserLogin, UserSignUp
from smart_cart.utils.auth import hash_password, verify_password

# User #


def test_user():
    password_to_hash = "password"
    user = user_factory(hashed_password=hash_password(password_to_hash)).model_dump()

    user_schema = User(**user)

    assert user_schema.user_id == user["user_id"]
    assert user_schema.email == user["email"]
    assert user_schema.hashed_password == user["hashed_password"]
    assert user_schema.first_name == user["first_name"]
    assert user_schema.last_name == user["last_name"]
    assert user_schema.created_at == user["created_at"]
    assert user_schema.updated_at == user["updated_at"]
    assert user_schema.last_login == user["last_login"]
    assert user_schema.is_active == user["is_active"]
    assert user_schema.is_superuser == user["is_superuser"]
    assert user_schema.is_staff == user["is_staff"]

    assert uuid.UUID(user_schema.user_id)

    assert user_schema.model_dump() == user

    assert verify_password(password_to_hash, user_schema.hashed_password)


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("user_id", 123),
        ("email", "invalid_email"),
        ("hashed_password", ""),
        ("first_name", ""),
        ("last_name", ""),
        ("created_at", "invalid_date"),
        ("updated_at", "invalid_date"),
        ("last_login", "invalid_date"),
        ("is_active", "invalid_bool"),
        ("is_superuser", "invalid_bool"),
        ("is_staff", "invalid_bool"),
    ],
)
def test_create_user_invalid(field, invalid_value):
    with pytest.raises(ValidationError):
        User(**{field: invalid_value})


def test_from_dynamodb_item(user_repository):
    expected_user = user_factory()

    user_repository.create_user(expected_user)

    item = user_repository.get_user(expected_user.user_id).model_dump()

    actual_user = User.from_dynamoItem(item)

    assert actual_user == expected_user


# UserSignUp #


def test_user_sign_up():
    user_sign_up = user_signup_factory().model_dump()

    user_sign_up_schema = UserSignUp(**user_sign_up)

    assert user_sign_up_schema.email == user_sign_up["email"]
    assert user_sign_up_schema.password == user_sign_up["password"]
    assert user_sign_up_schema.first_name == user_sign_up["first_name"]
    assert user_sign_up_schema.last_name == user_sign_up["last_name"]


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("email", "invalid_email"),
        ("password", ""),
        ("first_name", ""),
        ("last_name", ""),
    ],
)
def test_create_user_sign_up_invalid(field, invalid_value):
    with pytest.raises(ValidationError):
        UserSignUp(**{field: invalid_value})


# UserLogin #


def test_user_login():
    user_login = user_login_factory().model_dump()

    user_login_schema = UserLogin(**user_login)

    assert user_login_schema.email == user_login["email"]
    assert user_login_schema.password == user_login["password"]

    assert user_login_schema.model_dump() == user_login


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("email", "invalid_email"),
        ("password", ""),
    ],
)
def test_create_user_login_invalid(field, invalid_value):
    with pytest.raises(ValidationError):
        UserLogin(**{field: invalid_value})
