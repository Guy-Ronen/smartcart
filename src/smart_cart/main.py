from fastapi import FastAPI

from smart_cart.routers.health import router as health_router
from smart_cart.routers.login import router as login_router
from smart_cart.routers.receipts import router as receipts_router
from smart_cart.routers.root import router as root_router
from smart_cart.routers.signup import router as signup_router
from smart_cart.utils.middleware import TokenMiddleware

app = FastAPI()

app.include_router(root_router)
app.include_router(health_router)
app.include_router(signup_router, prefix="/api/v1")
app.include_router(login_router, prefix="/api/v1")
app.include_router(receipts_router, prefix="/api/v1")

app.add_middleware(TokenMiddleware)
