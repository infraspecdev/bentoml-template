import os
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware

load_dotenv()


class UpdateResponseHeaders(BaseHTTPMiddleware):
    """
    Middleware to update HTTP response headers.

    This middleware removes certain headers from the response and adds security-related
    headers if the environment is set to 'production'.
    """

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        if "x-bentoml-request-id" in response.headers:
            del response.headers["x-bentoml-request-id"]
        if "server" in response.headers:
            del response.headers["server"]

        if os.getenv("ENVIRONMENT") == "production":
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "deny"
            response.headers["Content-Security-Policy"] = "default-src 'none'"

        return response
