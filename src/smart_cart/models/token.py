import uuid

from pydantic import BaseModel


class TokenPayload(BaseModel):
    jti: str = str(uuid.uuid4())
    sub: str
    created_at: int
    expires_at: int
