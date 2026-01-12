"""
Seldon model wrapper for serving the sentiment analysis model.
"""

import logging
import os
from typing import Any, Dict, List, Union

import joblib
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentClassifier:
    """
    Seldon-compatible sentiment classifier.
    This class wraps the trained model for deployment with Seldon Core.
    """

    def __init__(self) -> None:
        """Initialize the classifier."""
        self.model = None
        self.ready = False

    def load(self) -> None:
        """Load the trained model."""
        model_path = os.getenv("MODEL_PATH", "/mnt/models/sentiment_model.pkl")
        logger.info(f"Loading model from {model_path}")

        try:
            self.model = joblib.load(model_path)
            self.ready = True
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def predict(
        self, X: Union[np.ndarray, List[str]], features_names: List[str] = None
    ) -> np.ndarray:
        """
        Make predictions on input data.

        Args:
            X: Input data (array of texts)
            features_names: Feature names (not used but required by Seldon)

        Returns:
            Predictions array
        """
        if not self.ready:
            raise RuntimeError("Model not loaded. Call load() first.")

        logger.info(f"Received prediction request with {len(X)} samples")

        try:
            # Convert to list if numpy array
            if isinstance(X, np.ndarray):
                texts = X.tolist()
            else:
                texts = X

            # Make predictions
            predictions = self.model.predict(texts)

            # Convert to numpy array
            result = np.array(predictions)
            logger.info(f"Predictions: {result}")

            return result

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise

    def predict_proba(
        self, X: Union[np.ndarray, List[str]], features_names: List[str] = None
    ) -> np.ndarray:
        """
        Predict class probabilities.

        Args:
            X: Input data (array of texts)
            features_names: Feature names (not used but required by Seldon)

        Returns:
            Class probabilities
        """
        if not self.ready:
            raise RuntimeError("Model not loaded. Call load() first.")

        try:
            # Convert to list if numpy array
            if isinstance(X, np.ndarray):
                texts = X.tolist()
            else:
                texts = X

            # Get probabilities
            probabilities = self.model.predict_proba(texts)

            return probabilities

        except Exception as e:
            logger.error(f"Probability prediction failed: {e}")
            raise

    def health_status(self) -> Dict[str, Any]:
        """
        Return health status.

        Returns:
            Health status dictionary
        """
        return {"ready": self.ready, "model_loaded": self.model is not None}
