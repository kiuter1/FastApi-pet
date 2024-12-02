from typing import Awaitable, Callable

from fastapi import HTTPException, Depends
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from src.api.v1.handlers.user import oauth2_scheme, get_current_auth_user



class AdminMiddleware(BaseHTTPMiddleware):
    __slots__ = ()

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        user = await get_current_auth_user(request)
        if user.is_admin:
            response = await call_next(request)
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough privileges",
            )

