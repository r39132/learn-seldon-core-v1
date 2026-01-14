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
make run                     # Start UI (requires Seldon deployed)
make stop                    # Stop UI server
make restart                 # Restart UI server
make notebook                # Start Jupyter notebook
```

### Code Quality
```bash
make precommit               # Run all code quality checks
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
| `src/seldon_model.py` | Seldon Core v1 Python wrapper |
| `src/train_model.py` | Model training |
| `models/sentiment_model.pkl` | Trained model |
| `k8s/seldon-deployment.yaml` | Seldon Core v1 deployment |
| `.s2i/environment` | Seldon s2i configuration |


## 🐛 Quick Troubleshooting

### UI cannot connect to Seldon
```bash
kubectl port-forward svc/sentiment-classifier-default -n seldon 8080:8000
# Then set SELDON_HOST=localhost and SELDON_PORT=8080
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

**See [SELDON_DEPLOYMENT.md](SELDON_DEPLOYMENT.md) for Seldon Core v1 deployment details**
