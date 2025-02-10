from unittest.mock import patch

import pytest

from smart_cart.utils.settings import (  # noqa: F401
    DeployedSettings,
    LocalSettings,
    TestSettings,
    get_settings,
)


@pytest.mark.parametrize(
    "environment, instance, secret_key",
    [
        ("test", "TestSettings", "test key"),
        ("local", "LocalSettings", "local key"),
    ],
)
def test_local_settings(monkeypatch, environment, instance, secret_key):
    monkeypatch.setenv("ENVIRONMENT", environment)

    settings = get_settings()

    assert isinstance(settings, eval(instance))
    assert settings.token_payload_secret_key == secret_key


def test_deployed_settings(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("TOKEN_PAYLOAD_SECRET_NAME", "mock_secret_name")

    with patch("smart_cart.utils.settings.DeployedSettings._get_secret") as mock_get_secret:
        mock_get_secret.return_value = "mock_secret_value"

        settings = get_settings()

    assert isinstance(settings, DeployedSettings)
    assert settings.token_payload_secret_key == "mock_secret_value"
