import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlmodel import SQLModel

from smart_cart.models.receipt import Receipt  # noqa
from smart_cart.models.user import User  # noqa


class DBSettings(BaseModel):
    username: str = os.getenv("POSTGRES_USER", "postgres")
    password: str = os.getenv("POSTGRES_PASSWORD", "password")
    endpoint: str = os.getenv("DB_ENDPOINT", "db")
    port: int = int(os.getenv("DB_PORT", 5432))
    name: str = os.getenv("POSTGRES_DB", "smart_cart")

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.endpoint}:{self.port}/{self.name}"


class TabsScannerSettings(BaseModel):
    process_endpoint: str = os.getenv("TABS_SCANNER_PROCESS_ENDPOINT", "")
    result_endpoint: str = os.getenv("TABS_SCANNER_RESULT_ENDPOINT", "")
    api_key: str = os.getenv("TABS_SCANNER_API_KEY", "")


class CommonSettings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "unknown-environment")
    token_payload_secret_key: str = ""
    hashing_algorithm: str = os.getenv("HASHING_ALGORITHM", "HS256")

    db: DBSettings = DBSettings()
    tabs_scanner: TabsScannerSettings = TabsScannerSettings()

    @property
    def engine(self):
        return create_engine(self.db.dsn, echo=False)

    def initialize_db(self):
        SQLModel.metadata.create_all(self.engine)


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
    def engine(self):
        return create_engine(self.db.dsn, echo=False)

    def initialize_db(self):
        SQLModel.metadata.create_all(self.engine)


def get_settings() -> CommonSettings:
    if os.getenv("ENVIRONMENT") in ["local", "test"]:
        return LocalSettings()
    else:
        return DeployedSettings()


settings: CommonSettings = get_settings()
settings.initialize_db()
engine = settings.engine
