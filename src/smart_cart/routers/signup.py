from fastapi import APIRouter, HTTPException, status

from smart_cart.models.user import User
from smart_cart.repositories.users import UserRepository
from smart_cart.utils.auth import create_access_token, hash_password

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: User):
    existing_user = UserRepository.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    user.hashed_password = hash_password(user.hashed_password)

    UserRepository.create_user(user)

    access_token = create_access_token(user)

    return {"access_token": access_token, "user": user.model_dump()}
