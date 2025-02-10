from typing import Optional

from sqlmodel import Field, Session, SQLModel, select

from smart_cart.database import engine
from smart_cart.models.user import User as UserModel
from smart_cart.utils.constants import DATETIME_NOW_TIMESTAMP


class User(SQLModel, table=True): # type: ignore
    user_id: str = Field(primary_key=True)
    email: str = Field(index=True)
    hashed_password: str = Field(min_length=8)
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    created_at: int
    updated_at: Optional[int] = None
    last_login: Optional[int] = None
    is_active: bool = Field(default=True, index=True)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)

    @classmethod
    def from_model(cls, item: dict) -> "User":
        return cls(
            user_id=item["user_id"],
            email=item["email"],
            hashed_password=item["hashed_password"],
            first_name=item["first_name"],
            last_name=item["last_name"],
            created_at=item["created_at"],
            updated_at=item.get("updated_at"),
            last_login=item.get("last_login"),
            is_active=item["is_active"],
            is_superuser=item["is_superuser"],
            is_staff=item["is_staff"],
        )


class UserRepository:
    @staticmethod
    def create_user(user: UserModel):
        with Session(engine) as session:
            db_user = User.from_model(user.model_dump())
            session.add(db_user)
            session.commit()

    @staticmethod
    def get_user(user_id: str) -> Optional[UserModel]:
        with Session(engine) as session:
            db_user = session.get(User, user_id)
            return UserModel(**db_user.model_dump()) if db_user else None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[UserModel]:
        with Session(engine) as session:
            statement = select(User).where(User.email == email)
            db_user = session.exec(statement).first()
            print(f"db_user: {db_user}")
            return UserModel(**db_user.model_dump()) if db_user else None

    @staticmethod
    def update_user(user: UserModel):
        with Session(engine) as session:
            db_user = session.get(User, user.user_id)
            if db_user:
                for key, value in user.model_dump().items():
                    setattr(db_user, key, value)
                session.commit()

    @staticmethod
    def delete_user(user_id: str):
        with Session(engine) as session:
            db_user = session.get(User, user_id)
            if db_user:
                session.delete(db_user)
                session.commit()

    @staticmethod
    def login_user(user: UserModel) -> User | UserModel:
        with Session(engine) as session:
            db_user = session.get(User, user.user_id)
            if db_user:
                db_user.last_login = DATETIME_NOW_TIMESTAMP
                db_user.is_active = True
                session.commit()
                session.refresh(db_user)
                return db_user
        return user
