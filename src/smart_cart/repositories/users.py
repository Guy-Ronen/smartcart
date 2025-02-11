from typing import Optional

from sqlmodel import Session, select

from smart_cart.models.user import User
from smart_cart.schemas.user import UserSchema
from smart_cart.utils.constants import DATETIME_NOW_TIMESTAMP
from smart_cart.utils.settings import engine


class UserRepository:
    @staticmethod
    def create_user(user: UserSchema):
        with Session(engine) as session:
            db_user = User.from_model(user.model_dump())
            session.add(db_user)
            session.commit()

    @staticmethod
    def get_user(user_id: str) -> Optional[UserSchema]:
        with Session(engine) as session:
            db_user = session.get(User, user_id)
            return UserSchema(**db_user.model_dump()) if db_user else None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[UserSchema]:
        with Session(engine) as session:
            statement = select(User).where(User.email == email)
            db_user = session.exec(statement).first()
            print(f"db_user: {db_user}")
            return UserSchema(**db_user.model_dump()) if db_user else None

    @staticmethod
    def update_user(user: UserSchema):
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
    def login_user(user: UserSchema) -> User | UserSchema:
        with Session(engine) as session:
            db_user = session.get(User, user.user_id)
            if db_user:
                db_user.last_login = DATETIME_NOW_TIMESTAMP
                db_user.is_active = True
                session.commit()
                session.refresh(db_user)
                return db_user
        return user
