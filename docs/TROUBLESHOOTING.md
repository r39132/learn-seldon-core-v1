# Troubleshooting Guide

This guide covers common issues and solutions for the Sentiment Analyzer project.

## Table of Contents

- [Tool Installation Issues](#tool-installation-issues)
- [Docker and Kubernetes Setup](#docker-and-kubernetes-setup)
- [Python Environment Issues](#python-environment-issues)
- [Runtime Issues](#runtime-issues)
- [Kubernetes Issues](#kubernetes-issues)
- [Seldon Core Issues](#seldon-core-issues)
- [Port Conflicts](#port-conflicts)

---

## Tool Installation Issues

### pyenv: "python: command not found"

**Problem:** Python commands don't work after installing pyenv.

**Solution:**
```bash
# Ensure pyenv is in PATH
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Make sure these lines are added to your shell configuration file (`~/.zshrc` or `~/.bash_profile`), then restart your terminal.

### jenv: "java: command not found"

**Problem:** Java commands don't work after installing jenv.

**Solution:**
```bash
# Add Java to jenv
jenv add /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
jenv global 17

# Verify
java -version
```

If the path doesn't exist, check where Homebrew installed Java:
```bash
brew info openjdk@17
```

### direnv: "direnv: error .envrc is blocked"

**Problem:** Environment variables aren't loading when entering the project directory.

**Solution:**
```bash
# Allow direnv in the project directory
direnv allow .
```

You need to explicitly allow direnv for each project directory for security reasons.

### uv: "command not found"

**Problem:** uv package manager is not found.

**Solution:**
```bash
# Install uv via brew
brew install uv

# Or use pip
pip install uv

# Verify installation
uv --version
```

---

## Docker and Kubernetes Setup

### Docker: "Cannot connect to the Docker daemon"

**Problem:** Docker commands fail because the daemon isn't running.

**Solution:**
```bash
# Ensure Docker Desktop is running
open -a Docker

# Wait for Docker to start, then verify
docker ps
```

Make sure Docker Desktop is configured to start on login in its preferences.

### minikube: "Exiting due to MK_USAGE: Docker driver with privileged mode"

**Problem:** minikube fails to start with Docker driver.

**Solution:**
```bash
# Delete existing cluster and start fresh
minikube delete
minikube start --driver=docker

# If that doesn't work, specify resources explicitly
minikube start --driver=docker --cpus=4 --memory=8192
```

### kubectl: "connection refused" or "server not found"

**Problem:** kubectl commands fail to connect to Kubernetes cluster.

**Solution:**
```bash
# Ensure minikube is running
minikube status

# If not running, start it
minikube start

# Verify kubectl can connect
kubectl get nodes
```

---

## Python Environment Issues

### Virtual environment not activating

**Problem:** `source .venv/bin/activate` fails or doesn't work.

**Solution:**
```bash
# Ensure virtual environment was created
ls -la .venv/

# If it doesn't exist, create it
uv venv --python 3.12.3

# Then activate
source .venv/bin/activate

# Verify you're in the venv
which python
```

### Package installation fails

**Problem:** `uv pip install` fails.

**Solution:**
```bash
# Ensure you're in the virtual environment
source .venv/bin/activate

# Try installing with more verbose output
uv pip install -e ".[dev]" -v

# If a specific package fails, try installing dependencies first
uv pip install wheel setuptools
```

### ImportError: No module named 'sklearn'

**Problem:** Import errors when running Python scripts.

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
uv pip install -e ".[dev]"

# Verify installation
python -c "import sklearn; print(sklearn.__version__)"
```

### Pre-commit hooks failing

**Problem:** Pre-commit hooks fail on git commit.

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Install pre-commit hooks
pre-commit install

# Run manually to see detailed errors
pre-commit run --all-files

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

---

## Runtime Issues

### Model Not Found

**Problem:** Application cannot find the trained model file.

**Solution:**
```bash
make train  # Train the model
```

The model file should be created at `models/sentiment_model.pkl`.

### UI Cannot Connect to Seldon

**Problem:** FastAPI UI cannot reach the Seldon Core API.

**Solution:**
```bash
# Set up port forwarding to Seldon service
kubectl port-forward svc/sentiment-classifier-default -n seldon 8080:8000

# Ensure environment variables are set correctly
# SELDON_HOST=localhost
# SELDON_PORT=8080
```

---

## Port Conflicts

**Problem:** Port 8000 or 8080 already in use.

**Check what's using the port:**
```bash
lsof -i :8000
lsof -i :8080
```

**Solution:**
```bash
# Stop the UI server
make stop-ui

# Or kill the process manually
kill -9 $(lsof -ti:8000)
```

---

## Kubernetes Issues

### Minikube Not Running

**Problem:** Kubernetes commands fail because minikube is not running.

**Solution:**
```bash
minikube start
```

### Pods Not Starting

**Problem:** Pods are in Pending, CrashLoopBackOff, or Error state.

**Diagnosis:**
```bash
# Check events
kubectl get events -n seldon --sort-by='.lastTimestamp'

# Check pod status and details
kubectl describe pod <pod-name> -n seldon

# View pod logs
kubectl logs <pod-name> -n seldon
```

**Common causes:**
- Insufficient resources (increase minikube memory/CPU)
- Image pull errors
- Missing configuration
- Model file not found

### Can't Access Services

**Problem:** Cannot access services deployed to Kubernetes.

**Solution:**
```bash
# Check service and endpoints
kubectl get svc,endpoints -n seldon

# Use minikube service (always works)
minikube service <service-name> -n seldon

# Or use port forwarding
kubectl port-forward svc/<service-name> -n seldon <local-port>:<service-port>
```

### Model File Missing in Kubernetes

**Problem:** Model file not found in minikube.

**Diagnosis:**
```bash
# Verify model file exists in minikube
minikube ssh "ls -la /tmp/models/"
```

**Solution:**
```bash
# Recopy model file to minikube
minikube cp models/sentiment_model.pkl /tmp/models/sentiment_model.pkl

# Restart deployment to pick up the file
kubectl rollout restart seldondeployment/sentiment-classifier -n seldon
```

---

## Seldon Core Issues

### SeldonDeployment Not Creating Pods

**Problem:** SeldonDeployment exists but no pods are created.

**Diagnosis:**
```bash
# Check SeldonDeployment status
kubectl get seldondeployments -n seldon
kubectl describe seldondeployment sentiment-classifier -n seldon
```

**Common causes:**
- Seldon Core operator not running
- Invalid SeldonDeployment spec
- Image not available

### Seldon Operator Not Running

**Problem:** Seldon Core operator is not active.

**Diagnosis:**
```bash
# Check operator status
kubectl get pods -n seldon-system

# View operator logs
kubectl logs -f deployment/seldon-controller-manager -n seldon-system
```

**Solution:**
```bash
# Reinstall Seldon Core
helm uninstall seldon-core -n seldon-system
helm install seldon-core seldonio/seldon-core-operator \
    --version 1.17.1 \
    --namespace seldon-system \
    --set usageMetrics.enabled=false \
    --set istio.enabled=false \
    --wait
```

### Image Pull Errors

**Problem:** Kubernetes cannot pull the Docker image.

**Diagnosis:**
```bash
# Check pod events
kubectl describe pod <pod-name> -n seldon
```

**Solution:**
```bash
# Ensure you're using minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild image in minikube
docker build -t sentiment-seldon:latest -f Dockerfile.seldon .

# Verify image exists
minikube ssh docker images | grep sentiment-seldon

# Make sure imagePullPolicy is set to IfNotPresent or Never in the deployment
```

### Seldon API Returns 404

**Problem:** Requests to Seldon API return 404 Not Found.

**Diagnosis:**
```bash
# Check if service is running
kubectl get svc -n seldon

# Check endpoint
kubectl get endpoints -n seldon
```

**Verify the correct API endpoint:**
- Seldon Core v1 API: `http://localhost:8080/api/v1.0/predictions`
- Service name: `sentiment-classifier-default`

**Solution:**
```bash
# Port forward to the correct service
kubectl port-forward svc/sentiment-classifier-default -n seldon 8080:8000

# Test with curl
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{"data":{"ndarray":[["This is amazing!"]]}}'
```

### Seldon Predictions Return Errors

**Problem:** Seldon API is reachable but returns error responses.

**Diagnosis:**
```bash
# View model server logs
make k8s-ms-logs

# Or directly
kubectl logs -f -l seldon-deployment-id=sentiment-classifier -n seldon
```

**Common causes:**
- Model file corrupted or incompatible
- Invalid request format
- Missing dependencies in Docker image
- Model initialization failed

---

## Getting More Help

If you encounter issues not covered here:

1. **Check logs:**
   ```bash
   make k8s-ms-logs          # Seldon model server logs
   kubectl get events -n seldon  # Kubernetes events
   ```

2. **Check status:**
   ```bash
   make k8s-ms-status        # Deployment status
   ```

3. **Review documentation:**
   - [QUICKSTART.md](QUICKSTART.md) - Quick start guide
   - [SETUP.md](SETUP.md) - Detailed setup instructions
   - [README.md](../README.md) - Project overview

4. **Check project issues:** Visit the GitHub repository issues page

5. **Clean start:** Sometimes a clean restart helps
   ```bash
   make k8s-clean            # Clean Kubernetes resources
   make clean-build-artifacts # Clean build artifacts
   make setup                # Re-run setup
   ```
