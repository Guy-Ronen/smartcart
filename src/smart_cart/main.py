from fastapi import FastAPI

from smart_cart.health import router as health_router

app = FastAPI()

app.include_router(health_router)
