from fastapi import APIRouter, HTTPException, status

from smart_cart.models.user import UserLogin
from smart_cart.repositories.users import UserRepository
from smart_cart.utils.auth import create_access_token, verify_password

router = APIRouter()


@router.post("/login")
def login(user_login: UserLogin, status_code=status.HTTP_200_OK):
    print("user_login:", user_login)
    user = UserRepository.get_user_by_email(user_login.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
