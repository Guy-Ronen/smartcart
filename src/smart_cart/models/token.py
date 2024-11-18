from pydantic import BaseModel


class TokenPayload(BaseModel):
    jti: str
    sub: str
    iat: int
    exp: int
