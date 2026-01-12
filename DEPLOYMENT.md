# Kubernetes Deployment Guide

## Architecture

The deployment consists of two main services:

1. **Sentiment Model Server** - FastAPI-based model serving endpoint
   - Serves the trained scikit-learn sentiment classifier
   - Exposes `/predict` and `/health` endpoints
   - Runs on port 8001 inside the cluster

2. **Sentiment UI** - FastAPI web application
   - Provides a user-friendly web interface
   - Proxies requests to the model server
   - Runs on port 8000 and exposed via NodePort 30080

## 🚀 Access the Application

**Recommended (macOS + Docker driver):**
```bash
minikube service sentiment-ui -n seldon
```
> Keep terminal open! Opens browser automatically.

**Alternative - Port Forward:**
```bash
kubectl port-forward -n seldon svc/sentiment-ui 8000:8000
```
> Then visit: http://localhost:8000

**NodePort (if accessible):**
```bash
minikube ip  # Get IP, then visit http://<ip>:30080
```

## 📊 Check Status

```bash
# All resources
kubectl get all -n seldon

# Just pods
kubectl get pods -n seldon

# Watch in real-time
kubectl get pods -n seldon -w
```

## 📝 View Logs

```bash
# UI logs
kubectl logs -f deployment/sentiment-ui -n seldon

# Model server logs
kubectl logs -f deployment/sentiment-model-server -n seldon
```

## 🔄 Redeploy After Model Changes

```bash
# Rebuild images (use minikube's Docker)
eval $(minikube docker-env)
docker build -t sentiment-model-server:latest -f Dockerfile.modelserver .
docker build -t sentiment-ui:latest -f Dockerfile.fastapi .

# Restart deployments
kubectl rollout restart deployment/sentiment-model-server -n seldon
kubectl rollout restart deployment/sentiment-ui -n seldon
```

## 🧪 Test the Model

**Via UI:**
1. Open browser to service URL
2. Enter: "This is absolutely amazing!"
3. Click Submit → Should show: **positive**

**Via API:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=This is great!"
```

## 🔧 Troubleshooting

**Pods not starting?**
```bash
kubectl describe pod <pod-name> -n seldon
kubectl logs <pod-name> -n seldon
```

**Model file missing?**
```bash
minikube ssh "ls -la /models/"
# If missing:
minikube cp models/sentiment_model.pkl /models/sentiment_model.pkl
kubectl rollout restart deployment/sentiment-model-server -n seldon
```

**Can't access UI?**
```bash
# Check service and endpoints
kubectl get svc,endpoints -n seldon

# Use minikube service (always works)
minikube service sentiment-ui -n seldon
```

## 🗑️ Clean Up

```bash
# Delete all resources
kubectl delete namespace seldon

# Stop minikube
minikube stop

# Delete minikube cluster
minikube delete
```
