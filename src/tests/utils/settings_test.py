from unittest.mock import patch

import pytest

from smart_cart.utils.settings import (
    DeployedSettings,
    LocalSettings,
    get_settings,
)


def test_local_settings(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "local")

    settings = get_settings()

    assert isinstance(settings, LocalSettings)
    assert settings.token_payload_secret_key == "local key"


def test_deployed_settings(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("TOKEN_PAYLOAD_SECRET_NAME", "mock_secret_name")

    with patch("smart_cart.utils.settings.DeployedSettings._get_secret") as mock_get_secret:
        mock_get_secret.return_value = "mock_secret_value"

        settings = get_settings()

    assert isinstance(settings, DeployedSettings)
    assert settings.token_payload_secret_key == "mock_secret_value"
