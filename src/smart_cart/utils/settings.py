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
    users_table_name: str = os.getenv("USERS_TABLE_NAME", "users")
    receipts_table_name: str = os.getenv("RECEIPTS_TABLE_NAME", "receipts")
    region: str = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_session_token: str = os.getenv("AWS_SESSION_TOKEN", "")
    host: str = os.getenv("HOST", "")

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


class TestSettings(CommonSettings):
    token_payload_secret_key: str = "test key"
    hashing_algorithm: str = "HS256"

    @property
    def database_dsn(self) -> str:
        return "sqlite:///:memory:"


def get_settings() -> CommonSettings:
    if os.getenv("ENVIRONMENT") == "test":
        return TestSettings()
    elif os.getenv("ENVIRONMENT") == "local":
        return LocalSettings()
    else:
        return DeployedSettings()


settings: CommonSettings = get_settings()
