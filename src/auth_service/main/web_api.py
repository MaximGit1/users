from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from auth_service.main.di.main import container_factory
from auth_service.presentation.base import get_routers_list
from auth_service.presentation.exc_handlers import setup_exc_handlers


def init_di(app: FastAPI) -> None:
    container = container_factory()

    setup_dishka(container, app)


def init_routers(app: FastAPI) -> None:
    app.include_router(*get_routers_list())


def create_app() -> FastAPI:
    app = FastAPI()

    init_di(app)
    init_routers(app)
    setup_exc_handlers(app)

    return app
