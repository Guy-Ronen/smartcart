from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: str
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    created_at: int
    updated_at: Optional[int] = None
    last_login: Optional[int] = None
    is_active: bool = True
    is_superuser: bool = False
    is_staff: bool = False

    @classmethod
    def from_dynamoItem(cls, item: dict) -> "User":
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


class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfileResponse(BaseModel):
    user_id: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool


class UserResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserProfileResponse
