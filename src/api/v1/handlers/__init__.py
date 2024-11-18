from fastapi import FastAPI

from .admin import router_admin


def setup_routers(app: FastAPI, router_list: list) -> None:
    for router in router_list:
        app.include_router(router)