from smart_cart.utils.factories import user_factory


def test_create_and_get_report(user_repository):

    expected_report = user_factory(user_id="123")

    user_repository.create_user(expected_report)

    actual_report = user_repository.get_user(expected_report.user_id)

    assert actual_report == expected_report


def test_get_report_not_found(user_repository):
    result = user_repository.get_user("non_existent_user_id")

    assert result is None
