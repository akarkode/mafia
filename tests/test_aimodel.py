import os
import pytest
from loguru import logger

from mafia.aimodel import BruteForceDetector

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../mafia/models/isolation_forest_model.pkl")

@pytest.fixture(scope="module")
def ai_detector():
    assert os.path.exists(MODEL_PATH), "Model file is missing. Run train_model.py first."
    return BruteForceDetector()

def test_model_metadata(ai_detector):
    metadata = ai_detector.metadata
    assert "model_version" in metadata
    assert "features_used" in metadata
    assert "trained_on" in metadata
    assert "score_range" in metadata
    logger.info("✅ test_model_metadata passed.")

def test_normal_behavior_prediction(ai_detector):
    risk_score = ai_detector.predict(attempt_count=3, avg_interval=5.0)
    logger.info(f"Risk Score (Normal Behavior): {risk_score}")
    assert risk_score < 0.5, "Risk score too high for normal behavior!"

def test_edge_behavior_prediction(ai_detector):
    risk_score = ai_detector.predict(attempt_count=10, avg_interval=1.0)
    logger.info(f"Risk Score (Edge Behavior): {risk_score}")
    assert 0.0 <= risk_score <= 1.0, "Risk score out of expected range!"

def test_brute_force_prediction(ai_detector):
    risk_score = ai_detector.predict(attempt_count=100, avg_interval=0.2)
    logger.info(f"Risk Score (Brute Force Attempt): {risk_score}")
    assert risk_score >= 0.7, "Brute force attempt not detected correctly!"
