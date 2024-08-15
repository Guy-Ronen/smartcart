import logging

from fastapi import APIRouter, Response

router = APIRouter()
logger = logging.getLogger(__name__)


def perform_health_check():
    return {"ok": True, "hello": "world"}


@router.get("/health")
async def health(response: Response):
    try:
        return perform_health_check()
    except Exception as e:
        logger.error(e)
        response.status_code = 500
        return {"ok": False, "error": str(e)}
