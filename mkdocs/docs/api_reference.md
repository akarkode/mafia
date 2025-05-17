
📖 API Reference

BruteForceMiddleware

| Parameter  | Type   | Description      |
|------------|--------|------------------|
| redis_url  | str    | Redis connection string |

BruteForceDetector
- .predict(attempt_count: int, avg_interval: float) -> float  
  Returns risk score between 0.0 and 1.0 based on trained Isolation Forest model.