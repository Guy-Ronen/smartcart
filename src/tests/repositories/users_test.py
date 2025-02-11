import pytest

from smart_cart.repositories.users import UserNotFoundError
from tests.factories.user import user_factory


def test_create_and_get_user(user_repository):
    expected_user = user_factory(user_id="123")
    user_repository.create_user(expected_user)
    actual_user = user_repository.get_user(expected_user.user_id)

    assert actual_user.user_id == expected_user.user_id
    assert actual_user.email == expected_user.email


def test_get_user_not_found(user_repository):
    result = user_repository.get_user("non_existent_user_id")
    assert result is None


def test_get_user_by_email(user_repository):
    expected_user = user_factory(email="guy.ronen@example.com")
    user_repository.create_user(expected_user)

    actual_user = user_repository.get_user_by_email(expected_user.email)

    assert actual_user.email == expected_user.email
    assert actual_user.user_id == expected_user.user_id


def test_get_user_by_email_not_found(user_repository):
    result = user_repository.get_user_by_email("nonexistent.email@example.com")
    assert result is None


def test_update_user(user_repository):
    user = user_factory()
    user_repository.create_user(user)

    user.email = "new.email@example.com"
    updated_user = user_repository.update_user(user)

    assert updated_user.email == "new.email@example.com"
    assert updated_user.user_id == user.user_id


def test_update_user_not_found(user_repository):
    user = user_factory(user_id="non_existent_user_id")
    with pytest.raises(UserNotFoundError):
        user_repository.update_user(user)


def test_login_user(user_repository):
    user = user_factory(is_active=False, last_login=None)
    user_repository.create_user(user)

    logged_in_user = user_repository.login_user(user.user_id)

    assert logged_in_user.is_active
    assert logged_in_user.last_login


def test_login_user_not_found(user_repository):
    with pytest.raises(UserNotFoundError):
        user_repository.login_user("non_existent_user_id")


def test_delete_user(user_repository):
    user = user_factory()
    user_repository.create_user(user)

    user_repository.delete_user(user.user_id)
    result = user_repository.get_user(user.user_id)

    assert result is None


def test_delete_user_not_found(user_repository):
    with pytest.raises(UserNotFoundError):
        user_repository.delete_user("non_existent_user_id")
