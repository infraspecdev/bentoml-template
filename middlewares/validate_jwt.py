import os
from http import HTTPStatus

import jwt
from dotenv import load_dotenv
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware

from utils.common.response import error_response
from utils.structure_logging.logger_config import logger

load_dotenv()


class JWTAuthentication(BaseHTTPMiddleware):
    """
    Middleware for JWT authentication. Checks if the request contains a valid JWT token
    in the Authorization header. If the token is missing or invalid, responds with an
    Unauthorized error. Handles expired tokens and other JWT-related errors.
    """

    async def dispatch(self, request, call_next):
        try:
            protected_routes = ["/api/v1/predict"]
            if request.url.path in protected_routes:
                if "Authorization" not in request.headers:
                    status_code = HTTPStatus.UNAUTHORIZED
                    error_msg = "Unauthorized access: Authorization header is missing in the request headers."
                    logger.error(error_msg, status_code=status_code)
                    return error_response(error_msg, status_code)

                token = request.headers.get("Authorization")
                jwt.decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"])

            response = await call_next(request)
            return response
        except ExpiredSignatureError:
            status_code = HTTPStatus.UNAUTHORIZED
            error_msg = "Unauthorized access: Expired JWT token"
            logger.error(error_msg, status_code=status_code)
            return error_response(error_msg, status_code)
        except InvalidTokenError:
            status_code = HTTPStatus.UNAUTHORIZED
            error_msg = "Unauthorized access: Invalid JWT token"
            logger.error(error_msg, status_code=status_code)
            return error_response(error_msg, status_code)
        except Exception:
            logger.exception("Internal server error while validating JWT")
            return error_response(
                "Internal Server Error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )
