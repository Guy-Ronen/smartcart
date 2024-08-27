import uuid

from smart_cart.models.token import TokenPayload
from smart_cart.utils.factories import token_payload_factory


def test_token_payload():
    token = token_payload_factory().model_dump()

    token_payload = TokenPayload(**token)

    assert token_payload.jti == token["jti"]
    assert token_payload.user_id == token["user_id"]
    assert token_payload.created_at == token["created_at"]
    assert token_payload.expires_at == token["expires_at"]

    assert uuid.UUID(token_payload.jti)

    assert token_payload.model_dump() == token
