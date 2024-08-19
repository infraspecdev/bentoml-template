import pytest
import jwt
import os
from unittest.mock import AsyncMock, Mock, patch
from http import HTTPStatus
from starlette.responses import JSONResponse
from middlewares.validate_jwt import JWTAuthentication
from utils.common.response import error_response


@pytest.fixture
def middleware():
    return JWTAuthentication(app=Mock())


@pytest.fixture
def mock_request():
    request = Mock()
    request.url.path = "/api/v1/predict"
    request.headers = {}
    return request


@pytest.fixture
def mock_response():
    return JSONResponse({"message": "success"})


@pytest.mark.asyncio
async def test_no_authorization_header(middleware, mock_request, mock_response, mocker):
    mock_call_next = AsyncMock(return_value=mock_response)
    logger_mock = mocker.patch("utils.structure_logging.logger_config.logger.error")

    response = await middleware.dispatch(mock_request, mock_call_next)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert (
        response.body
        == error_response(
            "Unauthorized access: Authorization header is missing in the request headers.",
            HTTPStatus.UNAUTHORIZED,
        ).body
    )
    logger_mock.assert_called_once_with(
        "Unauthorized access: Authorization header is missing in the request headers.",
        status_code=HTTPStatus.UNAUTHORIZED,
    )


@pytest.mark.asyncio
async def test_expired_jwt(
    middleware, mock_request, mock_response, monkeypatch, mocker
):
    mock_call_next = AsyncMock(return_value=mock_response)
    logger_mock = mocker.patch("utils.structure_logging.logger_config.logger.error")
    monkeypatch.setenv("JWT_SECRET", "test_secret")

    expired_token = jwt.encode({"exp": 0}, os.environ["JWT_SECRET"], algorithm="HS256")
    mock_request.headers = {"Authorization": expired_token}

    response = await middleware.dispatch(mock_request, mock_call_next)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert (
        response.body
        == error_response(
            "Unauthorized access: Expired JWT token", HTTPStatus.UNAUTHORIZED
        ).body
    )
    logger_mock.assert_called_once_with(
        "Unauthorized access: Expired JWT token", status_code=HTTPStatus.UNAUTHORIZED
    )


@pytest.mark.asyncio
async def test_invalid_jwt(
    middleware, mock_request, mock_response, monkeypatch, mocker
):
    mock_call_next = AsyncMock(return_value=mock_response)
    logger_mock = mocker.patch("utils.structure_logging.logger_config.logger.error")
    monkeypatch.setenv("JWT_SECRET", "test_secret")

    invalid_token = "invalid.token.here"
    mock_request.headers = {"Authorization": invalid_token}

    response = await middleware.dispatch(mock_request, mock_call_next)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert (
        response.body
        == error_response(
            "Unauthorized access: Invalid JWT token", HTTPStatus.UNAUTHORIZED
        ).body
    )
    logger_mock.assert_called_once_with(
        "Unauthorized access: Invalid JWT token", status_code=HTTPStatus.UNAUTHORIZED
    )


@pytest.mark.asyncio
async def test_internal_server_error(
    middleware, mock_request, mock_response, monkeypatch, mocker
):
    mock_call_next = AsyncMock(return_value=mock_response)
    logger_mock = mocker.patch("utils.structure_logging.logger_config.logger.exception")
    monkeypatch.setenv("JWT_SECRET", "test_secret")

    mocker.patch("jwt.decode", side_effect=Exception("Unexpected error"))

    valid_token = jwt.encode(
        {"some": "payload"}, os.environ["JWT_SECRET"], algorithm="HS256"
    )
    mock_request.headers = {"Authorization": valid_token}

    response = await middleware.dispatch(mock_request, mock_call_next)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert (
        response.body
        == error_response(
            "Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR
        ).body
    )
    logger_mock.assert_called_once_with("Internal server error while validating JWT")


@pytest.mark.asyncio
async def test_valid_jwt(middleware, mock_request, mock_response, monkeypatch):
    mock_call_next = AsyncMock(return_value=mock_response)
    monkeypatch.setenv("JWT_SECRET", "test_secret")

    valid_token = jwt.encode(
        {"some": "payload"}, os.environ["JWT_SECRET"], algorithm="HS256"
    )
    mock_request.headers = {"Authorization": valid_token}

    response = await middleware.dispatch(mock_request, mock_call_next)

    assert response.status_code == HTTPStatus.OK
    assert response.body == mock_response.body
