import time
from http.client import responses
from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

# не перевірка на адміна поки що
class AdminMiddleware(BaseHTTPMiddleware):
    __slots__ = ()

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        stop = time.perf_counter() - start

        response.headers["X-Process-Time"] = f"{stop:.5f}"

        return response

