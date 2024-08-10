import uuid

from pydantic import BaseModel


class TokenPayload(BaseModel):
    token_id: str = str(uuid.uuid4())
    user_id: str
    username: str
    email: str
    created_at: int
    expires_at: int
