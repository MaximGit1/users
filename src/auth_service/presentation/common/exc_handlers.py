from functools import partial as part
from typing import TYPE_CHECKING, cast

from starlette import status as code
from starlette.responses import JSONResponse

from auth_service.application.user.exceptions import (
    UserAlreadyExistsError,
    UserBannedError,
    UserInvalidCredentialsError,
    UserNotFoundError,
)
from auth_service.domain.user.exceptions import UserDomainValidationError

if TYPE_CHECKING:
    from fastapi import FastAPI
    from starlette.requests import Request

    class StubError(Exception):
        message: str


async def _validate(_: "Request", exc: Exception, status: int) -> JSONResponse:
    exc = cast("StubError", exc)
    return JSONResponse(content={"detail": exc.message}, status_code=status)


def init_exc_handlers(app: "FastAPI") -> None:
    app.add_exception_handler(
        UserDomainValidationError,
        part(_validate, status=code.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        UserAlreadyExistsError,
        part(_validate, status=code.HTTP_409_CONFLICT),
    )
    app.add_exception_handler(
        UserNotFoundError,
        part(_validate, status=code.HTTP_404_NOT_FOUND),
    )
    app.add_exception_handler(
        UserInvalidCredentialsError,
        part(_validate, status=code.HTTP_401_UNAUTHORIZED),
    )
    app.add_exception_handler(
        UserBannedError,
        part(_validate, status=code.HTTP_409_CONFLICT),
    )
