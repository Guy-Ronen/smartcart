import datetime
import uuid

from smart_cart.schemas.token import TokenPayload


def token_payload_factory(
    token_id: str = str(uuid.uuid4()),
    user_id: str = "user123",
    username: str = "John Doe",
    email: str = "john.doe@example.com",
    created_at: int = int(datetime.datetime.now().timestamp()),
    expires_at: int = int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp()),
):
    return TokenPayload(
        token_id=token_id,
        user_id=user_id,
        username=username,
        email=email,
        created_at=created_at,
        expires_at=expires_at,
    )
