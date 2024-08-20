# Monitoring

Monitoring is essential for ensuring the reliability, performance, and scalability of your API services. By using Prometheus metrics, you can gain valuable insights into your system's health and behavior.

## Prometheus Metrics

BentoML provides default metrics for the API server, accessible at http://localhost:3000/metrics. For more details on default metrics or to add custom metrics, please [refer to the BentoML documentation](https://docs.bentoml.com/en/v1.1.11/guides/metrics.html).

### Custom metrics configured

1. **bentoml_service_model_inferencing_duration_seconds:** This metric tracks the time taken for model inferencing requests.

   To calculate the 95th percentile of your BentoML service's model inference duration, use the following PromQL query:
   ```
   #promql
   histogram_quantile(0.95, sum(rate(bentoml_service_model_inferencing_duration_seconds_bucket[5m])) by (le))
   ```
   **Bucket Configuration:** The default bucket values are `buckets=(0.5, 1, 2.5, 5, 7.5, 10)`, representing the response time in seconds for how many requests fall into each bucket.

   If your model's response time is less than these values, update the bucket values incthe `utils/monitoring/prometheus_metrics.py` file accordingly.
   For instance, if your model's response time is between 0.1 and 0.5 seconds, you might use `buckets=(0.05, 0.1, 0.2, 0.3, 0.4, 0.5)`.
