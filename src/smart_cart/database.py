from sqlalchemy.pool import StaticPool  # Import StaticPool for SQLite in-memory
from sqlmodel import SQLModel, create_engine

from smart_cart.utils.settings import settings

DATABASE_URL = settings.database_dsn

if settings.environment == "test":
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)
else:
    engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
