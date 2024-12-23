import logging
import time
import traceback
from enum import IntEnum

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class BoundCode(IntEnum):
    INFORMATION = 199
    SUCCESSFUL = 299
    REDIRECT = 399
    CLIENT_ERROR = 499


HTTP_SERVER_ERROR_THRESHOLD = 500


class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time.time()

        try:
            request_body = await request.body()
        except Exception as body_exc:
            logger.warning("Error reading request body: %s", body_exc)
            request_body = None

        try:
            response = await call_next(request)
        except Exception as exc:
            exc_type = type(exc).__name__
            exc_message = str(exc)
            tb = traceback.format_exc()

            body_text = (
                request_body.decode("utf-8", errors="ignore")
                if request_body is not None
                else "No body"
            )

            logger.exception(
                "Unhandled exception occurred: %s\n"
                "Message: %s\n"
                "Traceback:\n%s\n"
                "Request body: %s",
                exc_type,
                exc_message,
                tb,
                body_text,
                extra={
                    "request_url": request.url,
                    "request_method": request.method,
                },
            )
            raise  # Pass the exception further to FastAPI

        end_time = f"{time.time() - start_time:.3f}s."
        client = request.client
        status_code = response.status_code

        if status_code >= HTTP_SERVER_ERROR_THRESHOLD:
            logger.error(
                "500 Server Error\n"
                "Request URL: %s\n"
                "Request Method: %s\n"
                "Response Status: %d\n"
                "Duration: %s\n"
                "Request body: %s",
                request.url,
                request.method,
                status_code,
                end_time,
                request_body.decode("utf-8", errors="ignore")
                if isinstance(request_body, bytes)
                else request_body,
                extra={},
            )

        extra = {
            "request_url": request.url,
            "request_method": request.method,
            "request_path": request.url.path,
            "request_size": int(request.headers.get("content-length", 0)),
            "request_host": f"{client.host}:{client.port}"
            if client
            else "",
            "response_status": status_code,
            "response_size": int(response.headers.get("content-length", 0)),
            "response_duration": end_time,
        }

        if status_code <= BoundCode.INFORMATION:
            logger.info("Information response", extra=extra)
        elif status_code <= BoundCode.SUCCESSFUL:
            logger.info("Success response", extra=extra)
        elif status_code <= BoundCode.REDIRECT:
            logger.info("Redirect response", extra=extra)
        elif status_code <= BoundCode.CLIENT_ERROR:
            logger.warning("Client request error", extra=extra)
        else:
            logger.error("Server response error", extra=extra)

        return response
