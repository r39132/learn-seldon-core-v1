#!/bin/bash
# Clean up Kubernetes deployments

set -e

echo "🧹 Cleaning up Kubernetes resources..."

# Delete deployments
echo "Deleting FastAPI deployment..."
kubectl delete -f k8s/fastapi-deployment.yaml --ignore-not-found=true

echo "Deleting Seldon deployment..."
kubectl delete -f k8s/seldon-deployment.yaml --ignore-not-found=true

echo "Deleting namespace..."
kubectl delete -f k8s/namespace.yaml --ignore-not-found=true

echo "✅ Cleanup complete!"
