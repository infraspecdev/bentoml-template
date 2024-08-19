"""
This module provides middleware for logging HTTP request and response details.

It defines the `RequestResponseHandler` class, which is responsible for logging request and response
details including request body, response body, and status codes.
The middleware also handles exceptions
that occur during request processing and logs them appropriately.

Key functionalities include:
- Logging request body for specified routes.
- Logging response body and status code.
- Handling and logging exceptions that occur during processing.
"""

import json
from http import HTTPStatus
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from utils.common.response import error_response
from utils.structure_logging.logger_config import logger


class RequestResponseException(Exception):
    """
    Custom exception for handling errors in request/response logging.

    Attributes:
        message (str): The error message.
        status_code (int): The HTTP status code associated with the error.
    """

    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class RequestResponseHandler(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.

    This middleware logs details of HTTP requests and responses, including request body,
    response body, and status codes. It also handles exceptions and logs them appropriately.

    Attributes:
        routes_to_log (list): List of API routes for which request and response logging is enabled.
    """

    @staticmethod
    async def async_iter(iterable):
        """
        Asynchronously iterates over an iterable.

        Args:
            iterable (iterable): The iterable to iterate over.

        Yields:
            item: The next item from the iterable.
        """
        for item in iterable:
            yield item

    @staticmethod
    async def log_request(request: Request):
        """
        Logs the request body if the method is POST, PUT, or PATCH.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            dict: The JSON body of the request if present.

        Raises:
            RequestResponseException: If the request body cannot be decoded as JSON.
        """
        try:
            if request.method not in ("POST", "PUT", "PATCH"):
                return None
            request_body = await request.body()
            if not request_body:
                return None

            req_body_json = json.loads(request_body)
            logger.warning("Request received", request=req_body_json)
            return req_body_json
        except json.JSONDecodeError:
            logger.exception("Failed to decode request body as JSON")
            raise RequestResponseException(
                message="Invalid JSON body", status_code=HTTPStatus.BAD_REQUEST
            )

    @staticmethod
    async def log_response(response: Response, req_body_json: dict):
        """
        Logs the response body and status code.

        Args:
            response (Response): The outgoing HTTP response.
            req_body_json (dict): The JSON body of the request.

        Raises:
            RequestResponseException: If the response body cannot be decoded as JSON.
        """
        try:
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = RequestResponseHandler.async_iter(response_body)
            response_text = b"".join(response_body).decode("utf-8")
            res_body_json = json.loads(response_text)
            logger.warning(
                "Request response log",
                request=req_body_json,
                response=res_body_json,
                status_code=response.status_code,
            )
        except json.JSONDecodeError:
            logger.exception("Failed to decode response body as JSON")
            raise RequestResponseException(
                message="Internal server error",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Processes the request and response, logging details and handling exceptions.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next middleware or route handler to call.

        Returns:
            Response: The outgoing HTTP response.

        Raises:
            RequestResponseException: If an error occurs while processing the request/response.
        """
        try:
            routes_to_log = ["/api/v1/predict"]
            if request.url.path not in routes_to_log:
                return await call_next(request)

            req_body_json = await self.log_request(request)
            response = await call_next(request)
            await self.log_response(response, req_body_json)
            return response
        except RequestResponseException as e:
            return error_response(e.message, status_code=e.status_code)
        except Exception:
            logger.exception("Error processing request/response")
            return error_response(
                "Internal server error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )
