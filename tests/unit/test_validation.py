import pytest
from pydantic import BaseModel, ValidationError
from utils.common.validations import route_validation_mapping, IrisRequestParams


def test_route_validation_mapping():
    assert route_validation_mapping() == {"/api/v1/predict": IrisRequestParams}


def test_iris_request_params_missing_sepal_length():
    with pytest.raises(ValidationError) as excinfo:
        IrisRequestParams(sepal_width=3.5, petal_length=1.4, petal_width=0.2)
    assert "Field required" in str(excinfo.value) or "missing" in str(excinfo.value)


def test_iris_request_params_invalid_type():
    with pytest.raises(ValidationError) as excinfo:
        IrisRequestParams(
            sepal_length="five", sepal_width=3.5, petal_length=1.4, petal_width=0.2
        )
    assert "Input should be a valid number" in str(
        excinfo.value
    ) or "value is not a valid float" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        IrisRequestParams(
            sepal_length=[5.1], sepal_width=3.5, petal_length=1.4, petal_width=0.2
        )
    assert "Input should be a valid number" in str(
        excinfo.value
    ) or "value is not a valid float" in str(excinfo.value)
