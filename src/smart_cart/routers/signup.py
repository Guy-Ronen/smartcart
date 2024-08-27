import uuid

from fastapi import APIRouter, HTTPException, status

from smart_cart.models.user import User, UserSignUp
from smart_cart.repositories.users import UserRepository
from smart_cart.utils.auth import create_access_token, hash_password
from smart_cart.utils.constants import DATETIME_NOW_TIMESTAMP

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user_signup: UserSignUp):
    existing_user = UserRepository.get_user_by_email(user_signup.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    hashed_password = hash_password(user_signup.password)

    user = User(
        user_id=str(uuid.uuid4()),
        username=user_signup.username,
        email=user_signup.email,
        hashed_password=hashed_password,
        first_name=user_signup.first_name,
        last_name=user_signup.last_name,
        created_at=DATETIME_NOW_TIMESTAMP,
        updated_at=None,
        last_login=None,
        is_active=True,
        is_superuser=False,
        is_staff=False,
    )

    access_token = create_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
        },
    }
