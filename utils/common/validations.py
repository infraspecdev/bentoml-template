"""
This module defines validation schemas using Pydantic for API requests.
"""

from pydantic import BaseModel, Field


class IrisRequestParams(BaseModel):
    """
    Defines the expected parameters for the Iris prediction API request.
    """

    sepal_length: float = Field(description="Sepal length in cm", gt=0)
    sepal_width: float = Field(description="Sepal width in cm", gt=0)
    petal_length: float = Field(description="Petal length in cm", gt=0)
    petal_width: float = Field(description="Petal width in cm", gt=0)


def route_validation_mapping():
    """
    Maps API endpoints to their corresponding validation schemas.
    """
    return {"/api/v1/predict": IrisRequestParams}
