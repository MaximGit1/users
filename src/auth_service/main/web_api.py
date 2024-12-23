import logging
from pathlib import Path

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from auth_service.main.di.main import container_factory
from auth_service.presentation.base_router import get_routers_list
from auth_service.presentation.common.exc_handlers import init_exc_handlers
from auth_service.presentation.common.middlewares.tracing import (
    TracingMiddleware,
)


def init_di(app: FastAPI) -> None:
    container = container_factory()

    setup_dishka(container, app)


def init_routers(app: FastAPI) -> None:
    app.include_router(*get_routers_list())


def create_app() -> FastAPI:
    app = FastAPI()

    log_file_path = (Path(__file__).parent / "../../../logs.log").resolve()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=log_file_path,
    )
    logging.info("Application is starting...")

    init_di(app)
    init_routers(app)
    init_exc_handlers(app)

    app.add_middleware(TracingMiddleware)

    return app
