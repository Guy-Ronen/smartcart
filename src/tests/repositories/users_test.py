from smart_cart.utils.factories import user_factory


def test_create_and_get_user(user_repository):

    expected_user = user_factory(user_id="123")

    user_repository.create_user(expected_user)

    actual_user = user_repository.get_user(expected_user.user_id)

    assert actual_user == expected_user


def test_get_user_not_found(user_repository):
    result = user_repository.get_user("non_existent_user_id")

    assert result is None


def test_get_user_by_email(user_repository):

    expected_user = user_factory(email="guy.ronen@example.com")

    user_repository.create_user(expected_user)

    actual_user = user_repository.get_user_by_email(expected_user.email)

    assert actual_user == expected_user


def test_get_user_by_email_not_found(user_repository):
    result = user_repository.get_user_by_email("nonexistent.email@example.com")
    assert result is None


def test_update_user(user_repository):
    user = user_factory()
    user_repository.create_user(user)

    user.email = "new.email@example.com"

    user_repository.update_user(user)

    updated_user = user_repository.get_user(user.user_id)

    assert updated_user.email == "new.email@example.com"


def test_login_user(user_repository):
    user = user_factory(is_active=False, last_login=None)

    user_repository.create_user(user)
    user_repository.login_user(user)

    updated_user = user_repository.get_user(user.user_id)

    assert updated_user.is_active
    assert updated_user.last_login
