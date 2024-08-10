import os

from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    token_payload_secret_key: str = ""


class DeployedSettings(CommonSettings):
    def __init__(self, **data):
        super().__init__(**data)
        self._fetch_secrets()

    def _fetch_secrets(self):
        self.token_payload_secret_key = self._get_secret(os.getenv("TOKEN_PAYLOAD_SECRET_NAME"))

    def _get_secret(self, secret_name: str):
        pass  # TODO implement fetching secret from AWS Secrets Manager


class LocalSettings(CommonSettings):
    token_payload_secret_key: str = "local key"


def get_settings() -> CommonSettings:
    if os.getenv("ENVIRONMENT") in ["local", "test"]:
        return LocalSettings()
    else:
        return DeployedSettings()


settings: CommonSettings = get_settings()
