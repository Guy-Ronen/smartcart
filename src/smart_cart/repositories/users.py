from typing import Optional

from sqlmodel import Session, select

from smart_cart.models.user import User
from smart_cart.schemas.user import UserSchema
from smart_cart.utils.constants import DATETIME_NOW_TIMESTAMP
from smart_cart.utils.settings import engine


class UserNotFoundError(Exception):
    pass


class UserRepository:
    @staticmethod
    def _get_session():
        return Session(engine)

    @staticmethod
    def _get_db_user_by_id(session: Session, user_id: str) -> Optional[User]:
        return session.get(User, user_id)

    @staticmethod
    def create_user(user: UserSchema) -> UserSchema:
        with UserRepository._get_session() as session:
            db_user = User.from_model(user.model_dump())
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return UserSchema(**db_user.model_dump())

    @staticmethod
    def get_user(user_id: str) -> Optional[UserSchema]:
        with UserRepository._get_session() as session:
            db_user = UserRepository._get_db_user_by_id(session, user_id)
            return UserSchema(**db_user.model_dump()) if db_user else None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[UserSchema]:
        with UserRepository._get_session() as session:
            statement = select(User).where(User.email == email)
            db_user = session.exec(statement).first()
            return UserSchema(**db_user.model_dump()) if db_user else None

    @staticmethod
    def update_user(user: UserSchema) -> UserSchema:
        with UserRepository._get_session() as session:
            db_user = UserRepository._get_db_user_by_id(session, user.user_id)
            if not db_user:
                raise UserNotFoundError(f"User with ID {user.user_id} not found.")

            for key, value in user.model_dump().items():
                setattr(db_user, key, value)

            session.commit()
            session.refresh(db_user)
            return UserSchema(**db_user.model_dump())

    @staticmethod
    def delete_user(user_id: str) -> None:
        with UserRepository._get_session() as session:
            db_user = UserRepository._get_db_user_by_id(session, user_id)
            if not db_user:
                raise UserNotFoundError(f"User with ID {user_id} not found.")

            session.delete(db_user)
            session.commit()

    @staticmethod
    def login_user(user_id: str) -> UserSchema:
        with UserRepository._get_session() as session:
            db_user = UserRepository._get_db_user_by_id(session, user_id)
            if not db_user:
                raise UserNotFoundError(f"User with ID {user_id} not found.")

            db_user.last_login = DATETIME_NOW_TIMESTAMP
            db_user.is_active = True
            session.commit()
            session.refresh(db_user)
            return UserSchema(**db_user.model_dump())
