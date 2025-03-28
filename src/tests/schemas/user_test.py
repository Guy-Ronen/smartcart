import uuid

import pytest
from pydantic import ValidationError

from smart_cart.schemas.user import (
    UserLogin,
    UserProfileResponse,
    UserResponse,
    UserSchema,
    UserSignUp,
)
from smart_cart.utils.auth import hash_password, verify_password
from tests.factories.user import user_factory, user_login_factory, user_signup_factory


def compare_schema_and_model_dump(schema, model_dump):
    for key, value in model_dump.items():
        assert getattr(schema, key) == value

    assert schema.model_dump() == model_dump


# UserSchema #


def test_user():
    password_to_hash = "password"
    user = user_factory(hashed_password=hash_password(password_to_hash)).model_dump()

    user_schema = UserSchema(**user)

    compare_schema_and_model_dump(user_schema, user)

    assert uuid.UUID(user_schema.user_id)

    assert user_schema.model_dump() == user

    assert verify_password(password_to_hash, user_schema.hashed_password)


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("user_id", 123),
        ("email", "invalid_email"),
        ("hashed_password", "1234567"),
        ("first_name", "1"),
        ("last_name", "1"),
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
        UserSchema(**{field: invalid_value})


# def test_from_dynamodb_item(user_repository):
# expected_user = user_factory()

# user_repository.create_user(expected_user)

# item = user_repository.get_user(expected_user.user_id).model_dump()

# actual_user = UserSchema.from_dynamoItem(item)

# assert actual_user == expected_user


# UserSignUp #


def test_user_sign_up():
    user_sign_up = user_signup_factory().model_dump()

    user_sign_up_schema = UserSignUp(**user_sign_up)

    compare_schema_and_model_dump(user_sign_up_schema, user_sign_up)


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

    compare_schema_and_model_dump(user_login_schema, user_login)

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


def test_user_profile_response():
    user = user_factory().model_dump()

    user_profile_response = UserProfileResponse(
        user_id=user["user_id"],
        email=user["email"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        is_active=user["is_active"],
    )

    assert user_profile_response.user_id == user["user_id"]
    assert user_profile_response.email == user["email"]
    assert user_profile_response.first_name == user["first_name"]
    assert user_profile_response.last_name == user["last_name"]
    assert user_profile_response.is_active == user["is_active"]


def test_user_response():
    user = user_factory().model_dump()

    user_profile_response = UserProfileResponse(
        user_id=user["user_id"],
        email=user["email"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        is_active=user["is_active"],
    )

    user_response = UserResponse(
        access_token="access_token",
        token_type="bearer",
        user=user_profile_response,
    )

    assert user_response.access_token == "access_token"
    assert user_response.token_type == "bearer"
    assert user_response.user == user_profile_response


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("access_token", ""),
        ("token_type", ""),
        ("user", ""),
    ],
)
def test_create_user_response_invalid(field, invalid_value):
    with pytest.raises(ValidationError):
        UserResponse(**{field: invalid_value})
