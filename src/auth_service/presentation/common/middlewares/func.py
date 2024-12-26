from collections.abc import Callable
from typing import Any

from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


def add_middleware(
    middleware_class: Callable[..., BaseHTTPMiddleware] | Any,
    *args: Any,
    **kwargs: Any,
) -> Middleware:
    return Middleware(middleware_class, *args, **kwargs)
