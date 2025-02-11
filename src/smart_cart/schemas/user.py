from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
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
