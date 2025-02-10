import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DBSettings(BaseModel):
    username: str = os.getenv("POSTGRES_USER", "postgres")
    password: str = os.getenv("POSTGRES_PASSWORD", "password")
    endpoint: str = os.getenv("DB_ENDPOINT", "db")
    port: int = int(os.getenv("DB_PORT", 5432))
    name: str = os.getenv("POSTGRES_DB", "smart_cart")


class CommonSettings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "unknown-environment")
    token_payload_secret_key: str = ""
    hashing_algorithm: str = os.getenv("HASHING_ALGORITHM", "HS256")

    db: DBSettings = DBSettings()

    @property
    def database_dsn(self) -> str:
        return f"postgresql://{self.db.username}:{self.db.password}@{self.db.endpoint}:{self.db.port}/{self.db.name}"


class DeployedSettings(CommonSettings):
    def __init__(self, **data):
        super().__init__(**data)
        self._fetch_secrets()

    def _fetch_secrets(self):
        self.token_payload_secret_key = self._get_secret(os.getenv("TOKEN_PAYLOAD_SECRET_NAME", ""))

    def _get_secret(self, secret_name: str):
        pass


class LocalSettings(CommonSettings):
    token_payload_secret_key: str = "local key"
    hashing_algorithm: str = "HS256"

    @property
    def database_dsn(self) -> str:
        return f"postgresql://{self.db.username}:{self.db.password}@{self.db.endpoint}:{self.db.port}/{self.db.name}"


def get_settings() -> CommonSettings:
    if os.getenv("ENVIRONMENT") in ["local", "test"]:
        return LocalSettings()
    else:
        return DeployedSettings()


settings: CommonSettings = get_settings()
