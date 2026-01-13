#!/bin/bash

set -e

echo "🚀 Deploying Sentiment Analyzer with Seldon Core to Kubernetes..."

# Check if minikube is running
if ! minikube status &> /dev/null; then
    echo "⚠️  Minikube is not running. Starting minikube..."
    minikube start --driver=docker --memory=4096 --cpus=2
fi

# Use minikube's Docker daemon
echo "🐳 Configuring Docker to use minikube..."
eval $(minikube docker-env)

# Build Docker image in minikube
echo "🔨 Building Seldon model image in minikube..."
docker build -t sentiment-seldon:latest -f Dockerfile.seldon .

# Copy model file to minikube
echo "📦 Copying model file to minikube..."
minikube ssh "sudo mkdir -p /tmp/models"
if [ -f models/sentiment_model.pkl ]; then
    minikube cp models/sentiment_model.pkl /tmp/models/sentiment_model.pkl
    echo "✅ Model file copied"
else
    echo "⚠️  Model file not found. Please run 'make train' first."
    exit 1
fi

# Create namespace
echo "📦 Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Check if Seldon Core is installed
echo "🔍 Checking for Seldon Core installation..."
if ! kubectl get crd seldondeployments.machinelearning.seldon.io &> /dev/null; then
    echo "📦 Installing Seldon Core v1.17.1..."
    kubectl create namespace seldon-system || true
    kubectl apply -f https://github.com/SeldonIO/seldon-core/releases/download/v1.17.1/seldon-core-operator.yaml

    echo "⏳ Waiting for Seldon Core operator to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/seldon-controller-manager -n seldon-system
    echo "✅ Seldon Core installed"
else
    echo "✅ Seldon Core is already installed"
fi

# Deploy SeldonDeployment
echo "🚀 Deploying SeldonDeployment..."
kubectl apply -f k8s/seldon-deployment.yaml

# Wait for deployment to be ready
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l seldon-deployment-id=sentiment-classifier -n seldon --timeout=300s || true

# Get service information
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Deployment Status:"
kubectl get seldondeployments -n seldon
echo ""
kubectl get pods -n seldon
echo ""
kubectl get svc -n seldon

# Get the service URL
echo ""
echo "🌐 To access the model:"
echo "  REST API: kubectl port-forward svc/sentiment-classifier-default -n seldon 8080:8000"
echo "  Then test: curl -X POST http://localhost:8080/api/v1.0/predictions -H 'Content-Type: application/json' -d '{\"data\":{\"ndarray\":[\"This is amazing!\"]}}}'"
echo ""
echo "📝 View logs:"
echo "  kubectl logs -f -l seldon-deployment-id=sentiment-classifier -n seldon"
echo ""
echo "🧹 To clean up:"
echo "  make k8s-clean"
