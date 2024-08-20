# BentoML Template

This repository contains the BentoML template for model API deployments.

## Prerequisites

Before you begin, ensure you have met the following requirements:

1. [install python](https://www.python.org/downloads/)
2. [install pip](https://pip.pypa.io/en/stable/installation/)
3. [install aws](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and login to your account.
4. A model stored in a S3 bucket in `.pickle` format.

## Usage

To use this template, clone the repository and customize it according to your model's requirements. Below is a quick start guide:

1. **Clone the repository:**

   ```sh
   git clone https://github.com/infraspecdev/bentoml-template.git
   cd bentoml-template
   ```
2. **Customize the template:**

   - Update `config.ini` to download the correct models from your S3 bucket.
   - Update `validations.py` to change the input validation for your model.
   - Update `service.py` to use your model.
   - Update `bentofile.yaml` If you have changed the service name in `service.py`.
3. **Run these commands to create a python environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. **Run these commands to install all the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
5. **Run these commands to start the service:**

   ```bash
   bentoml serve .
   ```

   This will start a local server at [http://localhost:3000](http://localhost:3000/)

## To run the model in docker or podman

1. **Build the bento model:**

   ```bash
   bentoml build .
   ```
2. **Build the image:**

   ```bash
   bentoml containerize summarization:<BUILD_VERSION>
   ```
3. **Run the container:**

   ```bash
   docker run --rm -p 8080:8080 summarization:<BUILD_VERSION>
   ```

The build version will be provided as the output of the `bentoml build` command. This will look something similar
to `IrisClassifierService:nftm2tqyagzp4mtu`. In this example, `nftm2tqyagzp4mtu` is the build
version. For this quickstart example, the name is `IrisClassifierService`, but you need to replace it with the name of your service class.
**Note:** Update the envs in the bentofile.yaml

```yaml
envs:
  - name: <ENV_VARIABLE_NAME>
    value: <VALUE>
```

## Environment Variables

### To configure env variables

1. Create a `.env` file with values similar to the given `.env.example` file.
2. Change the values in the `.env` according to your requirement.

### Details about the environment variables:

- **BENTOML_PORT:** Port on which the BentoML service will run.
- **JWT_SECRET:** Secret key used for signing JWT tokens. This should be a secure, randomly generated string.
- **JWT_EXPIRATION_MINUTES:** Duration (in minutes) for which the JWT token remains valid.
- **ENVIRONMENT:** Environment in which the service is running. Can be set to `development`, `staging`, or `production`.
- **LOG_LEVEL:** Logging level for the application. Can be set to `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.
  Default is `WARNING`.

## Download Models

To download the models from S3, update the bucket name and directory in the `configs/config.ini` file.

1. Replace `YOUR_S3_BUCKET_NAME` with the actual s3 bucket name.
2. Replace `YOUR_S3_BUCKET_DIRECTORY` with the directory path of the models in the s3.

The models can be downloaded by running:

```bash
python3 download_models.py
```

On a local machine, this will require AWS secret and access keys to download from S3.

## Updating `service.py` file

To deploy your specific model API using the provided BentoML template, you can follow the following points:

1. **Download or Import the Required Model and Libraries:** Replace the current file name for the model If you want to run a custom model or use import to import the model

```python
with open("./models/<YOUR_MODEL_FILE_NAME>", "rb") as model_file:
    model = pickle.load(model_file)
```

2. **Update the class name:** Change the class name to your model specific class name.

```python
class WeatherPrediciton
```

    You will need to update the class name in the`bentofile.yaml` also,
    ``yaml     service: "service:WeatherPrediciton"     ``

3. **Modify the API Route:** Update the API route to match the model's endpoint.

```python
@bentoml.api(route='/api/v1/analyze')
```

You will need to update the routes in following files as well.

```python
# middleware/validate_jwt.py
protected_routes = ['/api/v1/analyze']

# middlewares/request_response_handler.py
routes_to_log = ["/api/v1/analyze"]

# middlewares/validation_handler.py
routes_to_validate = ['/api/v1/analyze']

#utils/common/validations.py
return {"/api/v1/analyze": WeatherPredicitonParams}
```

4. **Update the Request Validation Schema:** Update the input validation(Params) in `utils/common/validations.py

```python
class IrisRequestParams(BaseModel):
    sepal_length: float = Field(description="Sepal length in cm", gt=0)
    sepal_width: float = Field(description="Sepal width in cm", gt=0)
    petal_length: float = Field(description="Petal length in cm", gt=0)
    petal_width: float = Field(description="Petal width in cm", gt=0)
```

The import statements, class name, route, inference logic, and middleware will be based on your specific use-case for model API development. The examples provided above are for reference only to give you an idea of the components you need to change.

In this example, we used a iris classifier model. If you are using a different
model or framework, these components might need to be completely different. You should code your class based on your specific requirements and the model you are using.

## JWT Authentication

In the quickstart sample, the `/api/v1/predict` endpoint requires the JWT token in the request authorization headers
to authenticate the request. If any other route which needs to be authenticated before serving the request, add the
endpoint in the `protected_routes` list in `middlewares/validate_jwt.py`.

To add more protected routes, update the `protected_routes` list:

```python
# middlewares/validate_jwt.py
protected_routes = [
	'/api/v1/predict',
	'/api/v1/analyze'
]
```

## Example curl request

```bash
curl -X 'POST' \
  'http://localhost:<BENTOML_PORT>/api/v1/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: <JWT_TOKEN>'  \
  -d '{
  "sepal_length": 1,
  "sepal_width": 2,
  "petal_length": 3,
  "petal_width": 4
}'
```

Replace ` <BENTOML_PORT>` and `<JWT_TOKEN>` with their values. Change `api/v1/summarize` and the request body with the new service route and new body if updated.
**To generate the JWT token:**

```bash
   python3 utils/jwt/generate_token.py
```

You can change the token expiry and secret by changing the environment variables `JWT_EXPIRATION_MINUTES`
and `JWT_SECRET` in the `.env` file.

* [ ] You can run this in your terminal to generate a `JWT_SECRET`.

```bash
date | base64 | base64
```

## Logging

[Structure Logging](utils/structure_logging/README.md#structure-logging)

## Monitoring

[Prometheus Metrics](utils/monitoring/README.md#prometheus-metrics)

## DynamoDB Setup

[Local DynamoDB Setup with Python](utils/dynamodb/README.md)
