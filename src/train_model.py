"""
Sentiment analysis model training script.
"""

import os
import pickle
from pathlib import Path
from typing import Any, Tuple

import joblib
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# Load environment variables
load_dotenv()


class SentimentModel:
    """Sentiment analysis model using Logistic Regression."""

    def __init__(
        self,
        max_features: int = 5000,
        ngram_range: Tuple[int, int] = (1, 2),
        random_state: int = 42,
    ) -> None:
        """
        Initialize the sentiment model.

        Args:
            max_features: Maximum number of features for TF-IDF
            ngram_range: N-gram range for TF-IDF
            random_state: Random state for reproducibility
        """
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.random_state = random_state

        # Create pipeline
        self.pipeline = Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        max_features=max_features,
                        ngram_range=ngram_range,
                        stop_words="english",
                    ),
                ),
                ("classifier", LogisticRegression(random_state=random_state, max_iter=1000)),
            ]
        )

    def train(self, X_train: pd.Series, y_train: pd.Series) -> None:
        """
        Train the model.

        Args:
            X_train: Training texts
            y_train: Training labels
        """
        print("Training model...")
        self.pipeline.fit(X_train, y_train)
        print("Training complete!")

    def predict(self, X: pd.Series) -> np.ndarray:
        """
        Make predictions.

        Args:
            X: Input texts

        Returns:
            Predicted labels
        """
        return self.pipeline.predict(X)

    def evaluate(self, X_test: pd.Series, y_test: pd.Series) -> None:
        """
        Evaluate the model.

        Args:
            X_test: Test texts
            y_test: Test labels
        """
        y_pred = self.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"\nAccuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    def save(self, path: str) -> None:
        """
        Save the model to disk.

        Args:
            path: Path to save the model
        """
        # Create directory if it doesn't exist
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        # Save model
        joblib.dump(self.pipeline, path)
        print(f"\nModel saved to {path}")

    @classmethod
    def load(cls, path: str) -> "SentimentModel":
        """
        Load a model from disk.

        Args:
            path: Path to the saved model

        Returns:
            Loaded SentimentModel instance
        """
        model = cls()
        model.pipeline = joblib.load(path)
        print(f"Model loaded from {path}")
        return model


def load_data(data_path: str) -> pd.DataFrame:
    """
    Load training data.

    Args:
        data_path: Path to the data file

    Returns:
        DataFrame with the data
    """
    print(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} samples")
    print(f"Columns: {df.columns.tolist()}")
    return df


def main() -> None:
    """Main training function."""
    # Get configuration from environment
    data_path = os.getenv("RAW_DATA_PATH", "data/raw") + "/sentiment_data.csv"
    model_path = os.getenv("MODEL_PATH", "models/sentiment_model.pkl")
    test_size = float(os.getenv("TRAIN_TEST_SPLIT", "0.2"))
    random_seed = int(os.getenv("RANDOM_SEED", "42"))
    max_features = int(os.getenv("MAX_FEATURES", "5000"))

    # Load data
    df = load_data(data_path)

    # Split data
    X = df["text"]
    y = df["sentiment"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_seed, stratify=y
    )

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    # Initialize and train model
    model = SentimentModel(max_features=max_features, random_state=random_seed)
    model.train(X_train, y_train)

    # Evaluate model
    model.evaluate(X_test, y_test)

    # Save model
    model.save(model_path)


if __name__ == "__main__":
    main()
