"""
Seldon Core v1 model wrapper for serving the sentiment analysis model.
This follows the Seldon Core v1 Python wrapper interface.
"""

import logging
import os
from typing import Any

import joblib
import numpy as np
from numpy.typing import NDArray

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentClassifier:
    """
    Seldon Core v1 compatible sentiment classifier.
    This class wraps the trained model for deployment with Seldon Core.

    The class implements the Seldon Python wrapper interface:
    - __init__(): Constructor, automatically called by Seldon
    - predict(): Main prediction method (required)
    - predict_proba(): Probability prediction (optional)
    - health_status(): Health check endpoint (optional)
    """

    def __init__(self) -> None:
        """
        Initialize and load the classifier.
        In Seldon Core v1, __init__ is called once when the container starts.
        """
        self.model = None
        self.ready = False

        # Load model immediately on initialization
        model_path = os.getenv("MODEL_PATH", "/mnt/models/sentiment_model.pkl")
        logger.info(f"Initializing SentimentClassifier, loading model from {model_path}")

        try:
            self.model = joblib.load(model_path)
            self.ready = True
            logger.info("Model loaded successfully in __init__")
        except Exception as e:
            logger.error(f"Failed to load model in __init__: {e}")
            raise

    def predict(
        self, X: NDArray | list | list[str], features_names: list[str] | None = None
    ) -> NDArray:
        """
        Make predictions on input data.
        This is the main method called by Seldon Core for inference.

        Args:
            X: Input data - can be:
               - numpy array of shape (n_samples, n_features) or (n_samples,)
               - list of strings
               - list of lists
            features_names: Feature names (not used but part of Seldon interface)

        Returns:
            Predictions as numpy array of shape (n_samples,)
        """
        if not self.ready or self.model is None:
            raise RuntimeError("Model not loaded")

        input_info = getattr(X, "shape", len(X) if hasattr(X, "__len__") else "unknown")
        logger.info(f"Received prediction request, input type: {type(X)}, shape/len: {input_info}")

        try:
            # Handle different input formats
            if isinstance(X, np.ndarray):
                # If 2D array with shape (n_samples, 1), flatten to get text strings
                if X.ndim == 2 and X.shape[1] == 1:
                    texts = X.flatten().tolist()
                elif X.ndim == 1:
                    texts = X.tolist()
                else:
                    # Already in the right format
                    texts = X
            elif isinstance(X, list):
                # If list of lists (from JSON), extract the strings
                if X and isinstance(X[0], list):
                    texts = [item[0] if isinstance(item, list) else item for item in X]
                else:
                    texts = X
            else:
                texts = X

            # Make predictions
            predictions = self.model.predict(texts)

            logger.info(f"Predictions shape: {predictions.shape}")
            return predictions

        except Exception as e:
            logger.error(f"Prediction failed: {e}", exc_info=True)
            raise

    def predict_proba(
        self, X: NDArray | list | list[str], features_names: list[str] | None = None
    ) -> NDArray:
        """
        Predict class probabilities.
        This method is optional but useful for getting confidence scores.

        Args:
            X: Input data (same format as predict())
            features_names: Feature names (not used but part of Seldon interface)

        Returns:
            Class probabilities as numpy array of shape (n_samples, n_classes)
        """
        if not self.ready or self.model is None:
            raise RuntimeError("Model not loaded")

        try:
            # Handle different input formats (same logic as predict)
            if isinstance(X, np.ndarray):
                if X.ndim == 2 and X.shape[1] == 1:
                    texts = X.flatten().tolist()
                elif X.ndim == 1:
                    texts = X.tolist()
                else:
                    texts = X
            elif isinstance(X, list):
                if X and isinstance(X[0], list):
                    texts = [item[0] if isinstance(item, list) else item for item in X]
                else:
                    texts = X
            else:
                texts = X

            # Get probabilities
            probabilities = self.model.predict_proba(texts)

            logger.info(f"Probability predictions shape: {probabilities.shape}")
            return probabilities

        except Exception as e:
            logger.error(f"Probability prediction failed: {e}", exc_info=True)
            raise

    def health_status(self) -> dict[str, Any]:
        """
        Return health status.

        Returns:
            Health status dictionary
        """
        return {"ready": self.ready, "model_loaded": self.model is not None}
