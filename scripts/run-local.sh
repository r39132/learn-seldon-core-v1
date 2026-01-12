#!/bin/bash
# Run locally without Kubernetes

set -e

echo "🚀 Running locally..."

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

# Start model server in the background
echo "🤖 Starting model server on port 8001..."
MODEL_PATH=models/sentiment_model.pkl uvicorn src.model_server:app --host 0.0.0.0 --port 8001 &
MODEL_SERVER_PID=$!

# Wait for model server to be ready
sleep 2

# Start FastAPI UI in the background
echo "🌐 Starting FastAPI UI on port 8000..."
uvicorn src.app:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

echo ""
echo "✅ Both servers started!"
echo "   Model Server: http://localhost:8001"
echo "   UI: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $MODEL_SERVER_PID $FASTAPI_PID; exit" INT
wait
