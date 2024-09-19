import uuid

from smart_cart.models.token import TokenPayload
from smart_cart.factories.token import token_payload_factory


def test_token_payload():
    token = token_payload_factory().model_dump()

    token_payload = TokenPayload(**token)

    assert token_payload.jti == token["jti"]
    assert token_payload.sub == token["sub"]
    assert token_payload.iat == token["iat"]
    assert token_payload.exp == token["exp"]

    assert uuid.UUID(token_payload.jti)

    assert token_payload.model_dump() == token
