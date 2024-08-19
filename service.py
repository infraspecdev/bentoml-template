from __future__ import annotations

import os
import pickle
import logging
import numpy as np
import bentoml

from middlewares.log_parameters import SetLogDefaultParameters
from middlewares.request_response_handler import RequestResponseHandler
from middlewares.validation_handler import ValidationHandler
from middlewares.validate_jwt import JWTAuthentication
from middlewares.update_response_headers import UpdateResponseHeaders
from utils.structure_logging.logger_config import configure_structure_logging
from utils.common.validations import IrisRequestParams

# Configure logging
configure_structure_logging()
bento_logger = logging.getLogger("bentoml")
bento_logger.setLevel(os.getenv("LOG_LEVEL", "WARNING").upper())

# Load the model
with open("./models/iris.pickle", "rb") as model_file:
    model = pickle.load(model_file)

bentoml.picklable_model.save_model("iris_knn_model", model)


@bentoml.service
class IrisClassifierService:
    """
    Service for classifying iris flowers using a k-nearest neighbors (KNN) model.

    This service exposes an API endpoint `/api/v1/predict` that takes input parameters for
    sepal length, sepal width, petal length, and petal width, and returns a prediction
    from the pre-trained KNN model.
    """

    def __init__(self) -> None:
        self.model = bentoml.picklable_model.load_model("iris_knn_model:latest")

    @bentoml.api(route="/api/v1/predict", input_spec=IrisRequestParams)
    def predict(self, **request_parameters: dict):
        """
        Predict the class of an iris flower based on input parameters.

        Parameters:
            request_parameters (dict): A dictionary containing input parameters for prediction.

        Returns:
            dict: A dictionary containing the prediction or an error message.
        """
        try:
            params = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
            values = [request_parameters.get(param) for param in params]

            if None in values:
                return {"message": "Missing one or more required parameters"}

            data_array = np.array([values], dtype=np.float32)
            prediction = self.model.predict(data_array)

            return {"prediction": prediction.tolist()[0]}
        except Exception:
            return {"message": "Internal Server Error"}


IrisClassifierService.add_asgi_middleware(SetLogDefaultParameters)
IrisClassifierService.add_asgi_middleware(RequestResponseHandler)
IrisClassifierService.add_asgi_middleware(ValidationHandler)
IrisClassifierService.add_asgi_middleware(JWTAuthentication)
IrisClassifierService.add_asgi_middleware(UpdateResponseHeaders)
