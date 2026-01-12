#!/bin/bash
# Deploy to Kubernetes (minikube)

set -e

echo "🚢 Deploying to Kubernetes..."

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "❌ Minikube is not running. Starting minikube..."
    minikube start
fi

# Set minikube docker env
echo "🐳 Configuring Docker environment..."
eval $(minikube docker-env)

# Build Docker images
echo "🔨 Building Docker images..."
docker build -t sentiment-model-server:latest -f Dockerfile.modelserver .
docker build -t sentiment-ui:latest -f Dockerfile.fastapi .

# Copy model to minikube
echo "📦 Copying model to minikube..."
minikube ssh "sudo mkdir -p /models"
MODEL_PATH="models/sentiment_model.pkl"
if [ -f "$MODEL_PATH" ]; then
    minikube cp "$MODEL_PATH" /models/sentiment_model.pkl
else
    echo "⚠️  Model not found at $MODEL_PATH. Please train the model first."
    exit 1
fi

# Create namespace
echo "📦 Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Deploy model server
echo "🤖 Deploying model server..."
kubectl apply -f k8s/model-server-deployment.yaml

# Wait for model server deployment
echo "⏳ Waiting for model server..."
kubectl wait --for=condition=available --timeout=300s deployment/sentiment-model-server -n seldon

# Deploy FastAPI UI
echo "🌐 Deploying FastAPI UI..."
kubectl apply -f k8s/fastapi-deployment.yaml

# Wait for FastAPI deployment
echo "⏳ Waiting for FastAPI deployment..."
kubectl wait --for=condition=available --timeout=300s deployment/sentiment-ui -n seldon

# Get service URLs
echo ""
echo "✅ Deployment complete!"
echo ""
echo "Access the application:"
MINIKUBE_IP=$(minikube ip)
echo "  FastAPI UI: http://${MINIKUBE_IP}:30080"
echo ""
echo "Useful commands:"
echo "  View pods: kubectl get pods -n seldon"
echo "  View logs (UI): kubectl logs -f deployment/sentiment-ui -n seldon"
echo "  View logs (Model Server): kubectl logs -f deployment/sentiment-model-server -n seldon"
echo "  Port forward UI: kubectl port-forward -n seldon svc/sentiment-ui 8000:8000"
echo "  Port forward Model: kubectl port-forward -n seldon svc/sentiment-model-server 8001:8001"
