#!/bin/bash
# Quick start script for first-time users

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Sentiment Analyzer with Seldon - Quick Start          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if setup has been run
if [ ! -d ".venv" ]; then
    echo "🚀 First time setup detected. Running initial setup..."
    echo ""
    ./scripts/setup.sh
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if model exists
if [ ! -f "models/sentiment_model.pkl" ]; then
    echo "📊 Generating training data..."
    python src/generate_data.py
    
    echo ""
    echo "🤖 Training model..."
    python src/train_model.py
    echo ""
fi

echo "✅ Everything is ready!"
echo ""
echo "Choose an option:"
echo ""
echo "  1. Test inference locally (CLI)"
echo "  2. Start FastAPI web server (local)"
echo "  3. Open Jupyter notebooks"
echo "  4. Deploy to Kubernetes (minikube)"
echo "  5. Run all tests"
echo "  6. Exit"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "🎭 Starting local inference..."
        echo "Tip: Try 'This product is amazing!' or 'Terrible quality!'"
        echo ""
        python src/inference.py
        ;;
    2)
        echo ""
        echo "🌐 Starting FastAPI server..."
        echo "Access the UI at: http://localhost:8000"
        echo ""
        uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
        ;;
    3)
        echo ""
        echo "📓 Starting Jupyter notebook..."
        jupyter notebook
        ;;
    4)
        echo ""
        echo "☸️  Deploying to Kubernetes..."
        ./scripts/deploy-k8s.sh
        ;;
    5)
        echo ""
        echo "🧪 Running all tests..."
        ./scripts/test-all.sh
        ;;
    6)
        echo ""
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
