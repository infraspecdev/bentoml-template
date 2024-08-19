"""
This module provides middleware for setting default logging parameters for HTTP requests.

It defines the `SetLogDefaultParameters` class, which clears and binds context variables for logging
each incoming request, including request ID, host, HTTP method, and API endpoint. This middleware
is used to ensure that log entries contain relevant context information for tracing and debugging.
"""

import uuid
from http import HTTPStatus
from typing import Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from utils.common.response import error_response
from utils.structure_logging.logger_config import logger


class SetLogDefaultParameters(BaseHTTPMiddleware):
    """
    Middleware for setting default logging parameters for requests.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Sets default logging parameters and processes the request.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next middleware or route handler to call.

        Returns:
            Response: The outgoing HTTP response.
        """
        try:
            structlog.contextvars.clear_contextvars()
            structlog.contextvars.bind_contextvars(
                request_id=str(uuid.uuid4()),
                host=request.headers.get("host", "unknown"),
                http_method=request.method,
                api_endpoint=request.url.path,
            )

            response = await call_next(request)
            return response
        except Exception:
            logger.exception("Error configuring log parameters")
            return error_response(
                "Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR
            )
