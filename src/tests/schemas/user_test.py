import uuid
from smart_cart.schemas.user import User
from smart_cart.utils.bcrypt import hash_password, verify_password
from smart_cart.utils.factories import user_factory


def test_user():
    password_to_hash = "password"
    user = user_factory(hashed_password=hash_password(password_to_hash)).model_dump()

    user_schema = User(**user)

    assert user_schema.id == user["id"]
    assert user_schema.username == user["username"]
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

    assert uuid.UUID(user_schema.id)

    assert user_schema.model_dump() == user

    assert verify_password(password_to_hash, user_schema.hashed_password)

