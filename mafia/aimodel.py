import os
import joblib
import numpy as np
from loguru import logger

class BruteForceDetector:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "models", "isolation_forest_model.pkl")
        if not os.path.exists(model_path):
            logger.error("Model file not found. Please train the model first.")
            raise FileNotFoundError("Model file not found. Please train the model first.")

        with open(model_path, "rb") as f:
            data = joblib.load(f)
            self.model = data["model"]
            self.metadata = data["metadata"]

        logger.success(f"🔖 Loaded model version: {self.metadata['model_version']} trained on {self.metadata['trained_on']}")

        # Load min-max score range from metadata or fallback to default
        if "score_range" in self.metadata:
            self.min_score, self.max_score = self.metadata["score_range"]
        else:
            logger.warning("Score range not found in metadata, using default values.")
            self.min_score = -0.5
            self.max_score = 0.5

    def predict(self, attempt_count: int, avg_interval: float) -> float:
        input_features = np.array([[attempt_count, avg_interval]])
        raw_score = self.model.decision_function(input_features)[0]
        logger.debug(f"Raw Decision Function Output: {raw_score}")
        risk_score = self._normalize_minmax(raw_score)

        logger.info(f"Prediction - Attempts: {attempt_count}, Interval: {avg_interval}s, Risk Score: {risk_score}")
        return risk_score

    def _normalize_minmax(self, raw_score: float) -> float:
        raw_score = max(min(raw_score, self.max_score), self.min_score)
        normalized = (raw_score - self.min_score) / (self.max_score - self.min_score)
        return round(normalized, 2)
