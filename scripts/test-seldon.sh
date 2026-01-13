#!/bin/bash

echo "🧪 Testing Seldon deployment..."

# Check if port-forward is running
if lsof -ti:8080 > /dev/null 2>&1; then
    echo "✅ Port forward detected on 8080"
else
    echo "⚠️  No port forward detected. Starting port-forward..."
    echo "Run this in another terminal: kubectl port-forward svc/sentiment-classifier-default -n seldon 8080:8000"
    exit 1
fi

echo ""
echo "📝 Testing prediction endpoint..."
echo ""

# Test with positive sentiment
echo "Test 1: Positive sentiment"
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{"data":{"ndarray":["This is absolutely amazing!"]}}'

echo -e "\n"

# Test with negative sentiment
echo "Test 2: Negative sentiment"
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{"data":{"ndarray":["This is terrible and awful."]}}'

echo -e "\n"

# Test with neutral sentiment
echo "Test 3: Neutral sentiment"
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{"data":{"ndarray":["The weather is moderate today."]}}'

echo -e "\n"

# Test batch prediction
echo "Test 4: Batch prediction"
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{"data":{"ndarray":["Great product!", "Not good", "It works fine"]}}'

echo -e "\n\n✅ Tests complete!"
