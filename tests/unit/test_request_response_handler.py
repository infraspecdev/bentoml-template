import pytest
import json
from http import HTTPStatus
from starlette.responses import Response
from unittest.mock import patch, AsyncMock, MagicMock

from middlewares.request_response_handler import (
    RequestResponseHandler,
    RequestResponseException,
)
from utils.structure_logging.logger_config import logger


async def test_log_request_post_method_valid_json():
    request = AsyncMock()
    request.url.path = "/api/v1/predict"
    request.method = "POST"
    request.body = AsyncMock(
        return_value=b'{"sepal_length": 1, "sepal_width": 2, "petal_length": 3, "petal_width": 4}'
    )

    with patch.object(logger, "warning") as mock_warning:
        handler = RequestResponseHandler(app=MagicMock())
        result = await handler.log_request(request)

        assert result == {
            "sepal_length": 1,
            "sepal_width": 2,
            "petal_length": 3,
            "petal_width": 4,
        }
        mock_warning.assert_called_once_with(
            "Request received",
            request={
                "sepal_length": 1,
                "sepal_width": 2,
                "petal_length": 3,
                "petal_width": 4,
            },
        )


async def test_log_request_invalid_json():
    request = AsyncMock()
    request.url.path = "/api/v1/predict"
    request.method = "POST"
    request.body = AsyncMock(return_value=b"invalid json")
    with patch.object(logger, "exception") as mock_exception:
        handler = RequestResponseHandler(app=MagicMock())

        with pytest.raises(RequestResponseException) as excinfo:
            await handler.log_request(request)

        assert excinfo.value.message == "Invalid JSON body"
        assert excinfo.value.status_code == HTTPStatus.BAD_REQUEST
        mock_exception.assert_called_once_with("Failed to decode request body as JSON")


async def test_log_response_valid_json():
    async def mock_body_iterator():
        yield b'{"sepal_length": 1, "sepal_width": 2, "petal_length": 3, "petal_width": 4}'

    response = AsyncMock()
    response.body_iterator = mock_body_iterator()
    response.status_code = HTTPStatus.OK
    req_body_json = {"request_key": "request_value"}

    with patch.object(logger, "warning") as mock_warning:
        handler = RequestResponseHandler(app=MagicMock())
        await handler.log_response(response, req_body_json)

        mock_warning.assert_called_once_with(
            "Request response log",
            request=req_body_json,
            response={
                "sepal_length": 1,
                "sepal_width": 2,
                "petal_length": 3,
                "petal_width": 4,
            },
            status_code=HTTPStatus.OK,
        )


async def test_log_response_invalid_json():
    async def mock_body_iterator():
        yield b"invalid json"

    response = AsyncMock()
    response.body_iterator = mock_body_iterator()
    response.status_code = HTTPStatus.OK
    req_body_json = {"request_key": "request_value"}

    with patch.object(logger, "exception") as mock_exception:
        handler = RequestResponseHandler(app=MagicMock())

        with pytest.raises(RequestResponseException) as excinfo:
            await handler.log_response(response, req_body_json)

        assert excinfo.value.message == "Internal server error"
        assert excinfo.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        mock_exception.assert_called_once_with("Failed to decode response body as JSON")


async def test_dispatch_valid_request_response():
    request = AsyncMock()
    request.url.path = "/api/v1/predict"
    request.method = "POST"
    request.body = AsyncMock(
        return_value=b'{"sepal_length": 1, "sepal_width": 2, "petal_length": 3, "petal_width": 4}'
    )
    response = Response(
        content=json.dumps({"response_key": "response_value"}),
        media_type="application/json",
    )

    async def mock_body_iterator():
        yield b'{"sepal_length": 1, "sepal_width": 2, "petal_length": 3, "petal_width": 4}'

    response.body_iterator = mock_body_iterator()

    call_next = AsyncMock(return_value=response)

    handler = RequestResponseHandler(app=MagicMock())

    with (
        patch.object(
            handler, "log_request", wraps=handler.log_request
        ) as mock_log_request,
        patch.object(
            handler, "log_response", wraps=handler.log_response
        ) as mock_log_response,
    ):
        result = await handler.dispatch(request, call_next)

        assert result.status_code == HTTPStatus.OK
        assert json.loads(result.body) == {"response_key": "response_value"}
        mock_log_request.assert_called_once_with(request)
        mock_log_response.assert_called_once_with(
            result,
            {"sepal_length": 1, "sepal_width": 2, "petal_length": 3, "petal_width": 4},
        )


async def test_dispatch_invalid_request():
    request = AsyncMock()
    request.url.path = "/api/v1/predict"
    request.method = "POST"
    request.body = AsyncMock(return_value=b"invalid json")

    call_next = AsyncMock()

    handler = RequestResponseHandler(app=MagicMock())

    with (
        patch.object(
            handler, "log_request", wraps=handler.log_request
        ) as mock_log_request,
        patch.object(
            handler, "log_response", wraps=handler.log_response
        ) as mock_log_response,
    ):
        result = await handler.dispatch(request, call_next)

        assert result.status_code == HTTPStatus.BAD_REQUEST
        assert json.loads(result.body) == {"message": "Invalid JSON body"}
        mock_log_request.assert_called_once_with(request)
        mock_log_response.assert_not_called()


async def test_dispatch_internal_error():
    request = AsyncMock()
    request.url.path = "/api/v1/predict"
    request.method = "POST"
    request.body = AsyncMock(
        return_value=b'{"sepal_length": 1, "sepal_width": 2, "petal_length": 3, "petal_width": 4}'
    )

    call_next = AsyncMock(side_effect=Exception("Unexpected error"))

    handler = RequestResponseHandler(app=MagicMock())

    with (
        patch.object(
            handler, "log_request", wraps=handler.log_request
        ) as mock_log_request,
        patch.object(
            handler, "log_response", wraps=handler.log_response
        ) as mock_log_response,
        patch.object(logger, "exception") as mock_logger_exception,
    ):
        result = await handler.dispatch(request, call_next)

        assert result.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert json.loads(result.body) == {"message": "Internal server error"}
        mock_log_request.assert_called_once_with(request)
        mock_log_response.assert_not_called()
        mock_logger_exception.assert_called_once_with(
            "Error processing request/response"
        )


async def test_dispatch_skipped_route():
    request = AsyncMock()
    request.method = "POST"
    request.url.path = "/not_to_log"
    request.body = AsyncMock(
        return_value=b'{"sepal_length": 1, "sepal_width": 2, "petal_length": 3, "petal_width": 4}'
    )

    call_next = AsyncMock()
    handler = RequestResponseHandler(app=MagicMock())

    with patch.object(
        handler, "log_request", wraps=handler.log_request
    ) as mock_log_request:
        await handler.dispatch(request, call_next)
        mock_log_request.assert_not_called()
        call_next.assert_called_once_with(request)


async def test_log_request_post_method_empty_body():
    request = AsyncMock()
    request.method = "POST"
    request.url.path = "/api/v1/predict"
    request.body = AsyncMock(return_value=b"")

    with patch.object(logger, "warning") as mock_warning:
        handler = RequestResponseHandler(app=MagicMock())
        result = await handler.log_request(request)

        assert result is None
        mock_warning.assert_not_called()


async def test_log_request_get_method():
    request = AsyncMock()
    request.method = "GET"
    request.url.path = "/api/v1/predict"
    request.body = AsyncMock(
        return_value=b'{"sepal_length": 1, "sepal_width": 2, "petal_length": 3, "petal_width": 4}'
    )

    with patch.object(logger, "warning") as mock_warning:
        handler = RequestResponseHandler(app=MagicMock())
        result = await handler.log_request(request)

        assert result is None
        mock_warning.assert_not_called()
