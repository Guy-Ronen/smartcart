import bcrypt
from smart_cart.utils.bcrypt import hash_password, verify_password


def test_hash_password():
    password = "password"
    hashed_password = hash_password(password)

    assert bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def test_verify_password():
    password = "password"
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    assert verify_password(password, hashed_password) is True
    assert verify_password("wrong_password", hashed_password) is False
