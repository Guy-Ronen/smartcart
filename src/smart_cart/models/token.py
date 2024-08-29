import uuid

from pydantic import BaseModel


class TokenPayload(BaseModel):
    jti: str = str(uuid.uuid4())
    sub: str
    iat: int
    exp: int
