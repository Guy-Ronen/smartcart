import jwt
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from smart_cart.models.token import TokenPayload
from smart_cart.utils.settings import settings


class TokenMiddleware(BaseHTTPMiddleware):

    whitelisted_endpoints = [
        "/health",
        "/redoc",
        "/openapi.json",
    ]

    def verify_token(self, token: str) -> TokenPayload | None:
        try:
            payload = TokenPayload(
                **jwt.decode(
                    token,
                    settings.token_payload_secret_key,
                    algorithms=["HS256"],
                )
            )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
        return payload

    async def dispatch(self, request: Request, call_next):
        if request.url.path not in self.whitelisted_endpoints:
            auth = request.headers.get("Authorization")
            if not auth or not auth.startswith("Bearer "):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Unauthorized"},
                )
            token = auth.replace("Bearer ", "")
            payload = self.verify_token(token)
            if not payload:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Unauthorized"},
                )

            request.state.user = payload
            if not self.check_user_data(request):
                raise HTTPException(status_code=403, detail="Forbidden")

        return await call_next(request)

    def check_user_data(self, request: Request) -> bool:
        user: TokenPayload = request.state.user

        if user.expires_at < user.created_at:
            return False
        return True
