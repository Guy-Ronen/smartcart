import datetime

WHITELISTED_ENDPOINTS = [
    "/health",
    "/redoc",
    "/openapi.json",
    "/api/v1/signup",
    "/api/v1/login",
]

DATETIME_NOW = datetime.datetime.now(datetime.UTC)
DATETIME_NOW_TIMESTAMP = int(datetime.datetime.now(datetime.UTC).timestamp())
