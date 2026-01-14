#!/bin/bash
# Run locally - starts UI only (use Seldon Core for model serving)

set -e

echo "🚀 Running Sentiment Analyzer UI..."

# Activate virtual environment
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Run scripts/setup.sh first."
    exit 1
fi

source .venv/bin/activate

# Check if model exists
if [ ! -f "models/sentiment_model.pkl" ]; then
    echo "⚠️  Model not found. Training model..."
    python src/train_model.py
fi

# Start FastAPI UI
echo "🌐 Starting FastAPI UI on port 8000..."
echo ""
echo "Note: For model serving, deploy to Seldon Core with:"
echo "  make k8s-deploy-seldon"
echo ""
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
