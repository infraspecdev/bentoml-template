from __future__ import annotations

import numpy as np
import bentoml
import pickle

from utils.common.validations import IrisRequestParams

with open('./models/iris.pickle', 'rb') as model_file:
    model = pickle.load(model_file)

bentoml.picklable_model.save_model('iris_knn_model', model)

@bentoml.service
class IrisClassifierService:
    def __init__(self) -> None:
        self.model = bentoml.picklable_model.load_model('iris_knn_model:latest')

    @bentoml.api(route='/api/v1/predict', input_spec=IrisRequestParams)
    def predict(self, ctx: bentoml.Context, **request_parameters: dict):
        try:
            params = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
            values = [request_parameters.get(param) for param in params]

            if None in values:
                return {'message': 'Missing one or more required parameters'}

            data_array = np.array([values], dtype=np.float32)
            prediction = self.model.predict(data_array)

            return {'prediction': prediction.tolist()[0]}
        except Exception:
            return {'message': 'Internal Server Error'}
