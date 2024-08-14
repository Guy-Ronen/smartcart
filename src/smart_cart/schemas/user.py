import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: str = str(uuid.uuid4())
    username: str
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    created_at: int = int(datetime.now().timestamp())
    updated_at: Optional[int] = None
    last_login: Optional[int] = None
    is_active: bool = True
    is_superuser: bool = False
    is_staff: bool = False
