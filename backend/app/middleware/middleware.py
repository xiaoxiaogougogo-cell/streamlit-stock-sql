import time
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.time()

        response = await call_next(request)

        duration = round(time.time() - start, 4)

        print(
            request.method,
            request.url.path,
            response.status_code,
            duration
        )

        return response
