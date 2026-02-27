import os
import joblib
import numpy as np

from loguru import logger
from datetime import datetime
from sklearn.ensemble import IsolationForest

# Training Data (Multi-Feature: [attempt_count, avg_interval_between_attempts])
X_train = np.array([
    [1, 5.0], [2, 3.0], [3, 2.0], [5, 1.5], [10, 1.0],  # Normal behavior
    [50, 0.5], [100, 0.2], [150, 0.1], [200, 0.05], [300, 0.01]  # Brute force scenarios
])

model = IsolationForest(
    contamination=0.1,  # Increased sensitivity
    n_estimators=200,
    random_state=42
)
model.fit(X_train)

# Analyze decision_function scores to determine realistic min and max values
scores = model.decision_function(X_train)
min_score, max_score = float(scores.min()), float(scores.max())
logger.info(f"Decision Function Score Range: min={min_score}, max={max_score}")

metadata = {
    "model_version": "v1.1",
    "trained_on": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    "features_used": ["attempt_count", "avg_interval_between_attempts"],
    "hyperparameters": {
        "contamination": 0.1,
        "n_estimators": 200
    },
    "score_range": [min_score, max_score]
}

# Save Model and Metadata
output_dir = "mafia/models"
os.makedirs(output_dir, exist_ok=True)
with open(os.path.join(output_dir, "isolation_forest_model.pkl"), "wb") as f:
    joblib.dump({"model": model, "metadata": metadata}, f)

logger.success("✅ Model trained and saved with updated score range metadata.")
