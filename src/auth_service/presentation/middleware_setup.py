from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .common.middlewares.func import add_middleware
from .common.middlewares.tracing import TracingMiddleware


def init_middleware(app: FastAPI) -> None:
    middlewares = [
        add_middleware(TracingMiddleware),
        add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["GET", "POST", "PATCH"],
            allow_headers=["Content-Type"],
            allow_credentials=True,
        ),
    ]

    for middleware in middlewares:
        app.add_middleware(
            middleware.cls, *middleware.args, **middleware.kwargs
        )
