from fastapi import APIRouter

from .user import router as user_router


def get_routers_list() -> list[APIRouter]:
    return [
        user_router,
    ]
