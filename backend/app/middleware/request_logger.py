import logging
from fastapi import Request

logger = logging.getLogger("uvicorn")


async def log_requests(request: Request, call_next):
    response = await call_next(request)

    if response.status_code >= 400:
        logger.warning(
            "%s %s -> %s",
            request.method,
            request.url.path,
            response.status_code
        )

    return responseo
