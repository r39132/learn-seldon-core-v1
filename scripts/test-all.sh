#!/bin/bash
# Test script to verify the entire setup

set -e

echo "🧪 Running comprehensive tests..."

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found. Run make setup first."
    exit 1
fi

# Test 1: Data Generation
echo "📊 Test 1: Data Generation"
python src/generate_data.py
if [ -f "data/raw/sentiment_data.csv" ]; then
    echo "✅ Data generation successful"
else
    echo "❌ Data generation failed"
    exit 1
fi

# Test 2: Model Training
echo "🤖 Test 2: Model Training"
python src/train_model.py
if [ -f "models/sentiment_model.pkl" ]; then
    echo "✅ Model training successful"
else
    echo "❌ Model training failed"
    exit 1
fi

# Test 3: Unit Tests
echo "🧪 Test 3: Unit Tests"
pytest
echo "✅ Unit tests passed"

# Test 4: Code Quality
echo "🔍 Test 4: Code Quality"
ruff check src/ tests/
echo "✅ Linting passed"

black --check src/ tests/
echo "✅ Formatting passed"

# Test 5: Type Checking
echo "📝 Test 5: Type Checking"
mypy src/ || echo "⚠️  Type checking has warnings (non-blocking)"

echo ""
echo "✅ All tests passed!"
echo ""
echo "Next steps:"
echo "  1. Start FastAPI: make run"
echo "  2. Deploy to K8s: make k8s-deploy"
