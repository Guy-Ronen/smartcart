import uuid

from pydantic import BaseModel


class TokenPayload(BaseModel):
    jti: str = str(uuid.uuid4())
    user_id: str
    email: str
    created_at: int
    expires_at: int
