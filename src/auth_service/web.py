from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from auth_service.infrastructure.database.models import map_tables
from auth_service.presentation.users import router as user_router
from auth_service.ioc import init_async_container


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def _setup_container(app: FastAPI, /) -> None:
    container = init_async_container()
    setup_dishka(container, app)


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=_lifespan,
        title="Auth service",
        description="Users & Auth",
        version="1.0.0",
        docs_url="/auth-docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    _setup_container(app)
    app.include_router(user_router)
    map_tables()
    return app


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv()
    app = create_app()

    uvicorn.run(app=app)
