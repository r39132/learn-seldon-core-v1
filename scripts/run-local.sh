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

# Start FastAPI UI
echo "🌐 Starting FastAPI UI on port 8000..."
echo ""
echo "Note: For model serving, deploy to Seldon Core with:"
echo "  make k8s-deploy-seldon"
echo ""
uvicorn src.sentiment_app_server:app --host 0.0.0.0 --port 8000 --reload
