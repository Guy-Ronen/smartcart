from fastapi import FastAPI

from smart_cart.routers.health import router as health_router
from smart_cart.utils.middleware import TokenMiddleware

app = FastAPI()

app.include_router(health_router)

app.add_middleware(TokenMiddleware)
