from fastapi import APIRouter, FastAPI

from .admin import router_admin

router = APIRouter()



router.include_router(router_admin)


def setup_routers(app: FastAPI) -> None:
    app.include_router(router)