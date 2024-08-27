#!/usr/bin/env python
import datetime
import os
import uuid

import jwt

from smart_cart.utils.constants import DATETIME_NOW, DATETIME_NOW_TIMESTAMP


def generate_jwt_token():
    token = jwt.encode(
        payload={
            "jti": str(uuid.uuid4()),
            "user_id": "user123",
            "email": "john.doe@example.com",
            "created_at": DATETIME_NOW_TIMESTAMP,
            "expires_at": int((DATETIME_NOW + datetime.timedelta(days=1)).timestamp()),
        },
        headers={
            "alg": "HS256",
        },
        key=os.getenv("TOKEN_PAYLOAD_SECRET_KEY"),
        algorithm="HS256",
    )
    return token


print(generate_jwt_token())
