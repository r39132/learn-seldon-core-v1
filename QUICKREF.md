# Quick Reference Guide

## 🚀 Common Commands

### Initial Setup
```bash
make setup                    # Run complete setup
source .venv/bin/activate    # Activate virtual environment
```

### Development
```bash
make data                    # Generate training data
make train                   # Train model
make run-local               # Run both UI + model server (recommended)
make run                     # Run FastAPI UI only (needs model server)
make run-model-server        # Run model server only
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

### Docker
```bash
make docker-build            # Build Docker images
docker images                # List images
```

### Kubernetes
```bash
make k8s-deploy              # Deploy to Kubernetes
make k8s-clean               # Clean up resources

kubectl get pods -n seldon                    # List pods
kubectl logs -f <pod-name> -n seldon         # View logs
kubectl describe pod <pod-name> -n seldon    # Describe pod
kubectl port-forward -n seldon svc/sentiment-ui 8000:8000  # Port forward
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

## 🔗 URLs

| Service | URL |
|---------|-----|
| FastAPI (local) | http://localhost:8000 |
| FastAPI (K8s) | http://$(minikube ip):30080 |
| Seldon API | http://localhost:9000 |

## 🐛 Quick Troubleshooting

### Issue: Virtual environment not found
```bash
./scripts/setup.sh
```

### Issue: Model not found
```bash
python src/train_model.py
```

### Issue: Port already in use
```bash
lsof -i :8000          # Find process
kill -9 <PID>          # Kill process
```

### Issue: Minikube not running
```bash
minikube start --cpus=4 --memory=8192
```

### Issue: Docker daemon error
```bash
eval $(minikube docker-env)
```

## 📦 Package Management

```bash
# Install new package
uv pip install <package>

# Install dev dependency
uv pip install --dev <package>

# Update package
uv pip install --upgrade <package>

# List installed packages
uv pip list
```

## 🔧 Git Commands

```bash
# Initialize repo
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo
gh repo create learn-seldon --public --source=. --remote=origin

# Push to GitHub
git push -u origin main

# Create feature branch
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push branch
git push origin feature/my-feature
```

## 🎯 Quick Test

```bash
# Test everything
./scripts/test-all.sh

# Or step by step
make data        # Generate data
make train       # Train model
make test        # Run tests
make run-local   # Start both servers
```

## 📊 Monitoring

```bash
# Watch pods
watch kubectl get pods -n seldon

# Stream logs
kubectl logs -f deployment/sentiment-ui -n seldon

# Resource usage
kubectl top pods -n seldon

# Minikube dashboard
minikube dashboard
```

## 🔄 Restart Services

```bash
# Restart FastAPI pod
kubectl rollout restart deployment/sentiment-ui -n seldon

# Restart Seldon deployment
kubectl rollout restart seldondeployment/sentiment-classifier -n seldon
```

## 💾 Backup & Export

```bash
# Export model
cp models/sentiment_model.pkl backups/

# Export data
cp data/raw/sentiment_data.csv backups/

# Export K8s configs
kubectl get all -n seldon -o yaml > k8s-backup.yaml
```

---

**Tip:** Use `make help` to see all available make targets!
