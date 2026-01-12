"""
Tests for FastAPI application.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


class TestFastAPIApp:
    """Test cases for FastAPI application."""

    @pytest.fixture
    def client(self) -> TestClient:
        """Create a test client."""
        return TestClient(app)

    def test_home_page(self, client: TestClient) -> None:
        """Test home page rendering."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Sentiment Analyzer" in response.text

    def test_health_check(self, client: TestClient) -> None:
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "sentiment-analyzer-ui"

    @patch("app.call_seldon_api")
    async def test_analyze_positive_sentiment(self, mock_seldon: AsyncMock, client: TestClient) -> None:
        """Test analyze endpoint with positive sentiment."""
        # Mock Seldon response
        mock_seldon.return_value = {"sentiment": "positive", "text": "Great product!"}

        response = client.post("/analyze", data={"text": "Great product!"})
        assert response.status_code == 200

    def test_analyze_empty_text(self, client: TestClient) -> None:
        """Test analyze endpoint with empty text."""
        response = client.post("/analyze", data={"text": ""})
        assert response.status_code == 200
        assert "Please enter some text" in response.text
