from pydantic import BaseModel, Field

class IrisRequestParams(BaseModel):
    sepal_length: float = Field(description="Sepal length in cm", gt=0)
    sepal_width: float = Field(description="Sepal width in cm", gt=0)
    petal_length: float = Field(description="Petal length in cm", gt=0)
    petal_width: float = Field(description="Petal width in cm", gt=0)

def route_validation_mapping():
    return {
        '/api/v1/predict': IrisRequestParams
    }
