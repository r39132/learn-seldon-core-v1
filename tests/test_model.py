"""
Tests for the sentiment model.
"""

import os
import sys
from pathlib import Path

import joblib
import numpy as np
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from train_model import SentimentModel


class TestSentimentModel:
    """Test cases for SentimentModel class."""

    @pytest.fixture
    def model(self) -> SentimentModel:
        """Create a model instance for testing."""
        return SentimentModel(max_features=100, random_state=42)

    @pytest.fixture
    def sample_data(self) -> tuple:
        """Create sample training data."""
        import pandas as pd

        texts = [
            "I love this product!",
            "This is amazing!",
            "Terrible quality",
            "Waste of money",
            "Excellent service",
            "Very disappointed",
        ]
        labels = ["positive", "positive", "negative", "negative", "positive", "negative"]
        return pd.Series(texts), pd.Series(labels)

    def test_model_initialization(self, model: SentimentModel) -> None:
        """Test model initialization."""
        assert model.max_features == 100
        assert model.random_state == 42
        assert model.pipeline is not None

    def test_model_training(self, model: SentimentModel, sample_data: tuple) -> None:
        """Test model training."""
        X, y = sample_data
        model.train(X, y)
        # Model should be able to make predictions after training
        predictions = model.predict(X[:2])
        assert len(predictions) == 2

    def test_model_prediction(self, model: SentimentModel, sample_data: tuple) -> None:
        """Test model prediction."""
        X, y = sample_data
        model.train(X, y)
        predictions = model.predict(X)
        assert len(predictions) == len(X)
        assert all(pred in ["positive", "negative"] for pred in predictions)

    def test_model_save_load(
        self, model: SentimentModel, sample_data: tuple, tmp_path: Path
    ) -> None:
        """Test model saving and loading."""
        X, y = sample_data
        model.train(X, y)

        # Save model
        model_path = tmp_path / "test_model.pkl"
        model.save(str(model_path))
        assert model_path.exists()

        # Load model
        loaded_model = SentimentModel.load(str(model_path))
        assert loaded_model.pipeline is not None

        # Compare predictions
        original_pred = model.predict(X)
        loaded_pred = loaded_model.predict(X)
        assert np.array_equal(original_pred, loaded_pred)
