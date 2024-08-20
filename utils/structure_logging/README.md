# Structure Logging

Logging is essential for monitoring and debugging your model API deployment. In our setup, we use the `warning` level to log information. This helps filter out noisy debug or info logs commonly seen in production environments where the log level is typically set to `warning`, `error`, or `exception`.

This approach allows us to maintain the necessary logs for analysis while reducing unnecessary noise.

## Usage

- **Import:** To use the logger, import it as shown below:
  ```python
  from utils.structure_logging.logger_config import logger
  ```

- **For Exception Handling:** Use the following pattern to log exceptions:
  ```python
  logger.exception('Internal Server Error')
  ```
- **For Other Relevant Logs:** Utilize the following pattern to log request and response details, including
  model predictions or any other relevant information:
  ```python
  logger.warning("Model Prediction", output=model_prediction_result)
  ```

## Current Limitations

- **JSON Formatting:** BentoML's default logger does not support JSON formatting in the current release (v1.3.2). This limitation may affect the consistency of log formatting across different components.

- **Log Level Consistency:** Setting a log level through BentoML may not consistently apply to all code paths. Some parts of the BentoML codebase may enforce log levels differently than others.

**Source:**
BentoML community Slack channel ([link](https://bentoml.slack.com/archives/CKRANBHPH/p1716802490310329)).

## Additional Configuration

For further customization or modification of logging behavior, refer to the structured logging configuration in
the `utils/structure_logging/logger_config.py` file.

For documentation, Refer [Structlog](https://www.structlog.org/en/stable/why.html)
