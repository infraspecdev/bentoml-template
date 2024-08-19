# utils/monitoring/prometheus_metrics.py

from prometheus_client import Histogram

# Initialize the metric once
bentoml_service_model_inferencing_duration_seconds = Histogram(
    name="bentoml_service_model_inferencing_duration_seconds",
    documentation="Time taken to perform inference",
    labelnames=["endpoint", "service_name"],
    unit="seconds",
    buckets=(0.5, 1, 2.5, 5, 7.5, 10),
)
