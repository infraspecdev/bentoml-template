from http import HTTPStatus
from unittest.mock import patch, Mock, AsyncMock
import pytest
from starlette.requests import Request
from starlette.responses import Response

from middlewares.log_parameters import SetLogDefaultParameters
from utils.common.response import error_response


@pytest.fixture
def mock_request():
    return Mock(spec=Request)


@pytest.fixture
def mock_call_next():
    return AsyncMock(return_value=Response())


@pytest.fixture
def middleware():
    return SetLogDefaultParameters(app=Mock())


@pytest.mark.asyncio
async def test_log_parameters_set(middleware, mock_request, mock_call_next):
    with (
        patch("uuid.uuid4", return_value="test-uuid"),
        patch("structlog.contextvars.clear_contextvars") as mock_clear_contextvars,
        patch("structlog.contextvars.bind_contextvars") as mock_bind_contextvars,
    ):

        response = await middleware.dispatch(mock_request, mock_call_next)

        mock_clear_contextvars.assert_called_once()
        mock_bind_contextvars.assert_called_once_with(
            request_id="test-uuid",
            host=mock_request.headers.get("host"),
            http_method=mock_request.method,
            api_endpoint=mock_request.url.path,
        )

        assert response == mock_call_next.return_value


@pytest.mark.asyncio
async def test_error_handling_in_middleware(middleware, mock_request):
    mock_call_next = AsyncMock(side_effect=Exception("Test Exception"))
    with patch("utils.structure_logging.logger_config.logger.exception") as mock_logger:

        response = await middleware.dispatch(mock_request, mock_call_next)

        expected_response = error_response(
            "Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR
        )
        assert response.status_code == expected_response.status_code
        assert response.body == expected_response.body

        mock_logger.assert_called_once_with("Error configuring log parameters")
