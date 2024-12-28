from fastapi import APIRouter, FastAPI

from .auth.router import router as auth_router
from .user.router import router as user_router


def get_routers_list() -> list[APIRouter]:
    return [
        auth_router,
        user_router,
    ]


def init_routers(app: FastAPI) -> None:
    for router in get_routers_list():
        app.include_router(router)
