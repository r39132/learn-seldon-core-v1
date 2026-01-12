"""
Tests for data generation.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from generate_data import SentimentDataGenerator


class TestSentimentDataGenerator:
    """Test cases for SentimentDataGenerator class."""

    @pytest.fixture
    def generator(self) -> SentimentDataGenerator:
        """Create a generator instance for testing."""
        return SentimentDataGenerator(num_samples=100, seed=42)

    def test_generator_initialization(self, generator: SentimentDataGenerator) -> None:
        """Test generator initialization."""
        assert generator.num_samples == 100
        assert len(generator.positive_templates) > 0
        assert len(generator.negative_templates) > 0
        assert len(generator.products) > 0

    def test_generate_samples(self, generator: SentimentDataGenerator) -> None:
        """Test sample generation."""
        samples = generator.generate_samples()
        assert len(samples) == 100
        assert all(isinstance(item, tuple) and len(item) == 2 for item in samples)
        assert all(label in ["positive", "negative"] for _, label in samples)

    def test_balanced_samples(self, generator: SentimentDataGenerator) -> None:
        """Test that samples are roughly balanced."""
        samples = generator.generate_samples()
        positive_count = sum(1 for _, label in samples if label == "positive")
        negative_count = sum(1 for _, label in samples if label == "negative")
        # Should be roughly 50/50
        assert abs(positive_count - negative_count) <= 1

    def test_save_to_csv(self, generator: SentimentDataGenerator, tmp_path: Path) -> None:
        """Test saving to CSV."""
        output_path = tmp_path / "test_data.csv"
        generator.save_to_csv(str(output_path))
        assert output_path.exists()

        # Verify CSV content
        df = pd.read_csv(output_path)
        assert len(df) == 100
        assert "text" in df.columns
        assert "sentiment" in df.columns

    def test_save_to_json(self, generator: SentimentDataGenerator, tmp_path: Path) -> None:
        """Test saving to JSON."""
        import json

        output_path = tmp_path / "test_data.json"
        generator.save_to_json(str(output_path))
        assert output_path.exists()

        # Verify JSON content
        with open(output_path) as f:
            data = json.load(f)
        assert len(data) == 100
        assert all("text" in item and "sentiment" in item for item in data)
