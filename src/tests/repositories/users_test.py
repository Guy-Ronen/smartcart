from smart_cart.utils.factories import user_factory


def test_create_and_get_report(user_repository):

    expected_report = user_factory(user_id="123")

    user_repository.create_user(expected_report)

    actual_report = user_repository.get_user(expected_report.user_id)

    assert actual_report == expected_report


def test_get_report_not_found(user_repository):
    result = user_repository.get_user("non_existent_user_id")

    assert result is None


def test_get_user_by_email(user_repository):

    expected_report = user_factory(email="guy.ronen@example.com")

    user_repository.create_user(expected_report)

    actual_report = user_repository.get_user_by_email(expected_report.email)

    assert actual_report == expected_report


def test_get_user_by_email_not_found(user_repository):
    result = user_repository.get_user_by_email("nonexistent.email@example.com")
    assert result is None
