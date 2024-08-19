from http import HTTPStatus
from pydantic import ValidationError
from unittest.mock import AsyncMock, MagicMock, patch

from middlewares.validation_handler import ValidationHandler
from utils.structure_logging.logger_config import logger


@patch("middlewares.validation_handler.route_validation_mapping")
async def test_valid_request(mock_route_validation_mapping):
    mock_validation_strategy = MagicMock()
    mock_route_validation_mapping.return_value = {
        "/api/v1/predict": mock_validation_strategy
    }
    request = AsyncMock()
    request.url.path = "/api/v1/predict"
    request.json = AsyncMock(return_value={"key": "value"})

    call_next = AsyncMock()
    handler = ValidationHandler(app=MagicMock())

    await handler.dispatch(request, call_next)

    mock_route_validation_mapping.assert_called_once()
    mock_validation_strategy.model_validate.assert_called_once_with({"key": "value"})
    call_next.assert_called_once()


@patch("middlewares.validation_handler.route_validation_mapping")
async def test_invalid_request(mock_route_validation_mapping):
    mock_validation_strategy = MagicMock()
    mock_route_validation_mapping.return_value = {
        "/api/v1/predict": mock_validation_strategy
    }
    request = AsyncMock()
    request.url.path = "/api/v1/predict"
    request.json = AsyncMock(return_value={"key": "value"})
    mock_errors = [
        {
            "type": "missing",
            "loc": ("text",),
            "msg": "Field required",
            "input": {
                "gt_int": 21,
            },
            "url": "https://errors.pydantic.dev/2/v/missing",
        }
    ]
    mock_validation_strategy.model_validate.side_effect = (
        ValidationError.from_exception_data("Invalid req body", mock_errors)
    )

    call_next = AsyncMock()
    handler = ValidationHandler(app=MagicMock())

    with patch.object(logger, "exception") as mock_logger:
        response = await handler.dispatch(request, call_next)

    mock_route_validation_mapping.assert_called_once()
    mock_validation_strategy.model_validate.assert_called_once_with({"key": "value"})
    mock_logger.assert_called_once_with("Invalid request body")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        response.body
        == b'{"message":"Invalid request body","errors":[{"field":"text","message":"Field required"}]}'
    )


@patch("middlewares.validation_handler.route_validation_mapping")
async def test_unvalidated_route(mock_route_validation_mapping):
    mock_validation_strategy = MagicMock()
    mock_route_validation_mapping.return_value = {
        "/api/v1/predict": mock_validation_strategy
    }
    request = AsyncMock()
    request.url.path = "/api/v1/others"

    call_next = AsyncMock()
    handler = ValidationHandler(app=MagicMock())

    await handler.dispatch(request, call_next)

    mock_validation_strategy.assert_not_called()


@patch("middlewares.validation_handler.route_validation_mapping")
async def test_unexpected_exception(mock_route_validation_mapping):
    mock_validation_strategy = MagicMock()
    mock_route_validation_mapping.return_value = {
        "/api/v1/predict": mock_validation_strategy
    }
    request = AsyncMock()
    request.url.path = "/api/v1/predict"
    request.json = AsyncMock(return_value={"key": "value"})

    call_next = AsyncMock()
    handler = ValidationHandler(app=MagicMock())

    with (
        patch.object(
            mock_validation_strategy,
            "model_validate",
            side_effect=Exception("test exception"),
        ) as mock_model_validate,
        patch.object(logger, "exception") as mock_logger,
    ):
        response = await handler.dispatch(request, call_next)

    mock_route_validation_mapping.assert_called_once()
    mock_model_validate.assert_called_once_with({"key": "value"})
    mock_logger.assert_called_once_with("Error validating request")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.body == b'{"message":"Internal Server Error"}'
