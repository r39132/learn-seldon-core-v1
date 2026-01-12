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
make docker-build            # Build Docker images
make k8s-deploy              # Deploy to Kubernetes
make k8s-clean               # Clean up resources
```

## 📂 Important Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `pyproject.toml` | Dependencies and config |
| `src/app.py` | FastAPI application |
| `src/train_model.py` | Model training |
| `models/sentiment_model.pkl` | Trained model |
| `k8s/seldon-deployment.yaml` | K8s deployment |


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

---

**See [DEPLOYMENT.md](DEPLOYMENT.md) for full Kubernetes documentation**
