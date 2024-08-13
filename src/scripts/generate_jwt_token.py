#!/usr/bin/env python
import datetime
import os
import uuid

import jwt


def generate_jwt_token():
    token = jwt.encode(
        payload={
            "token_id": str(uuid.uuid4()),
            "user_id": "user123",
            "username": "John Doe",
            "email": "john.doe@example.com",
            "created_at": int(datetime.datetime.now().timestamp()),
            "expires_at": int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp()),
        },
        headers={
            "alg": "HS256",
        },
        key=os.getenv("TOKEN_PAYLOAD_SECRET_KEY"),
        algorithm="HS256",
    )
    return token


print(generate_jwt_token())
