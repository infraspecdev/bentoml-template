"""
This module provides utility functions for creating JSON responses.
"""

from starlette.responses import JSONResponse


def error_response(
    error_msg: str, status_code: int, error_details: list = None
) -> JSONResponse:
    """
    Creates a JSON response for error messages.

    :param error_msg: The error message to include in the response.
    :param status_code: HTTP status code for the response.
    :param error_details: Optional list of error details.
    :return: A JSONResponse object containing the error message.
    """
    if error_details:
        return JSONResponse(
            content={"message": error_msg, "errors": error_details},
            status_code=status_code,
        )
    return JSONResponse(content={"message": error_msg}, status_code=status_code)
