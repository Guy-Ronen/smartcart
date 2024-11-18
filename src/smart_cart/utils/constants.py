import datetime

import bcrypt

WHITELISTED_ENDPOINTS = [
    "/health",
    "/redoc",
    "/openapi.json",
    "/api/v1/signup",
    "/api/v1/login",
]

# Datetime constants
DATETIME_NOW = datetime.datetime.now(datetime.UTC)
DATETIME_NOW_TIMESTAMP = int(datetime.datetime.now(datetime.UTC).timestamp())

# User constants
FIXED_USER_ID = "df96b767-107f-4789-abd9-b669ace362ea"
FIXED_EMAIL = "user_fixed@example.com"
FIXED_PASSWORD = "password"
FIXED_HASHED_PASSWORD = bcrypt.hashpw(FIXED_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
FIXED_TIMESTAMP = 1731311609
