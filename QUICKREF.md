# Quick Reference Guide

## 🚀 Common Commands

### Initial Setup
```bash
make setup                   # Run complete setup
```

### Development
```bash
make data                    # Generate training data
make train                   # Train model
make run                     # Start both UI + model server
make stop                    # Stop all servers
make restart                 # Restart servers
make notebook                # Start Jupyter notebook
```

### Testing & Quality
```bash
make test                    # Run tests
make test-cov                # Run tests with coverage
make lint                    # Run linting
make format                  # Format code
make pre-commit              # Run all pre-commit hooks
```

### Docker & Kubernetes
```bash
make docker-build            # Build all Docker images
make docker-build-seldon     # Build only Seldon model image
make k8s-deploy              # Deploy FastAPI version to K8s
make k8s-deploy-seldon       # Deploy Seldon Core v1 to K8s
make k8s-clean               # Clean up resources
```

## 📂 Important Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `pyproject.toml` | Dependencies and config |
| `src/app.py` | FastAPI UI application |
| `src/model_server.py` | FastAPI model server (non-Seldon) |
| `src/seldon_model.py` | Seldon Core v1 Python wrapper |
| `src/train_model.py` | Model training |
| `models/sentiment_model.pkl` | Trained model |
| `k8s/seldon-deployment.yaml` | Seldon Core v1 deployment |
| `k8s/model-server-deployment.yaml` | FastAPI deployment |
| `.s2i/environment` | Seldon s2i configuration |


## 🐛 Quick Troubleshooting

### Port already in use
```bash
make stop                  # Stop all servers
```

### Model not found
```bash
make train                 # Retrain model
```

### Minikube not running
```bash
minikube start
```

## 📊 Kubernetes Commands

### FastAPI Deployment
```bash
# View resources
kubectl get all -n seldon

# Stream logs
kubectl logs -f deployment/sentiment-ui -n seldon

# Access UI
minikube service sentiment-ui -n seldon

# Restart deployment
kubectl rollout restart deployment/sentiment-model-server -n seldon
```

### Seldon Core v1 Deployment
```bash
# View SeldonDeployment
kubectl get seldondeployments -n seldon

# View pods
kubectl get pods -n seldon -l seldon-deployment-id=sentiment-classifier

# Port forward
kubectl port-forward svc/sentiment-classifier-default -n seldon 8080:8000

# Test API
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{"data":{"ndarray":["This is amazing!"]}}'

# View model logs
kubectl logs -f -l seldon-deployment-id=sentiment-classifier -c classifier -n seldon

# View orchestrator logs
kubectl logs -f -l seldon-deployment-id=sentiment-classifier -c seldon-container-engine -n seldon
```

---

**See [DEPLOYMENT.md](DEPLOYMENT.md) for FastAPI deployment and [SELDON_DEPLOYMENT.md](SELDON_DEPLOYMENT.md) for Seldon Core v1**
