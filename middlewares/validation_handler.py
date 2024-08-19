from http import HTTPStatus
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from utils.common.formatters import format_error_message
from utils.common.response import error_response
from utils.common.validations import route_validation_mapping
from utils.structure_logging.logger_config import logger


class ValidationHandler(BaseHTTPMiddleware):
    """
    Middleware for validating request bodies against predefined schemas.
    """

    async def dispatch(self, request, call_next):
        """
        Process the request, validate the request body if needed,
        and pass the request to the next handler.

        Args:
            request (Request): The incoming request object.
            call_next (Callable): The next function to call in the ASGI application.

        Returns:
            Response: The response object returned by the next handler.
        """
        routes_to_validate = ["/api/v1/predict"]

        try:
            url_path = request.url.path
            if url_path in routes_to_validate:
                validation_strategy_mapping = route_validation_mapping()
                validation_strategy = validation_strategy_mapping.get(url_path)
                request_body = await request.json()
                validation_strategy.model_validate(request_body)

            response = await call_next(request)
            return response
        except ValidationError as e:
            logger.exception("Invalid request body")
            return error_response(
                error_msg="Invalid request body",
                error_details=format_error_message(e.errors()),
                status_code=HTTPStatus.BAD_REQUEST,
            )
        except Exception:
            logger.exception("Error validating request")
            return error_response(
                "Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR
            )
