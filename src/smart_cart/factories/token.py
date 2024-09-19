import datetime
import uuid
from typing import Optional

from smart_cart.models.token import TokenPayload
from smart_cart.utils.constants import DATETIME_NOW, DATETIME_NOW_TIMESTAMP


def token_payload_factory(
    jti: Optional[str] = None,
    sub: str = "user123",
    iat: Optional[int] = None,
    exp: Optional[int] = None,
):
    jti = jti or str(uuid.uuid4())
    iat = iat or DATETIME_NOW_TIMESTAMP
    exp = exp or int((DATETIME_NOW + datetime.timedelta(days=1)).timestamp())

    return TokenPayload(
        jti=jti,
        sub=sub,
        iat=iat,
        exp=exp,
    )
