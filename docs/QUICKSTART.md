# Quick Start Guide

Get up and running with the Sentiment Analyzer in minutes.

## Prerequisites

- macOS with [Homebrew](https://brew.sh) installed
- Docker Desktop (for Kubernetes deployment)
- 4GB+ RAM available for minikube

## Step 1: Setup

Clone and run setup:

```bash
# Clone repository
gh repo clone <username>/learn-seldon-core-v1
cd learn-seldon-core-v1

# Run automated setup
make setup
```

The setup script will:
- Install pyenv, jenv, direnv, uv, gh CLI
- Install Python 3.12.3 and Java 17
- Create virtual environment
- Install all dependencies
- Set up pre-commit hooks

**Important:** After setup completes, configure your shell:

```bash
# Add to ~/.zshrc or ~/.bash_profile
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

export PATH="$HOME/.jenv/bin:$PATH"
eval "$(jenv init -)"

eval "$(direnv hook zsh)"  # or: eval "$(direnv hook bash)"
```

Restart your terminal, then:

```bash
cd learn-seldon-core-v1
direnv allow .
```

For detailed setup instructions, see [SETUP.md](SETUP.md).

## Step 2: Generate Data and Train Model

```bash
make data   # Generate training dataset
make train  # Train sentiment model
```

This creates:
- `data/raw/sentiment_data.csv` - Training dataset
- `models/sentiment_model.pkl` - Trained model file

## Step 3: Deploy to Kubernetes

Deploy the model server with Seldon Core v1:

```bash
make k8s-deploy-model-server
```

This will:
- Start minikube (if not running)
- Build Docker image in minikube
- Copy model file to minikube
- Install Seldon Core v1.17.1 (if not installed)
- Deploy sentiment classifier

**Check deployment status:**

```bash
make k8s-ms-status
```

You should see:
- SeldonDeployment: `sentiment-classifier`
- Pods: Running (2/2 containers ready)
- Services: `sentiment-classifier-default`

## Step 4: Test the Model Server

**Set up port forwarding to access the Seldon API:**

```bash
# In a separate terminal
make k8s-ms-port-fwd
```

This forwards `localhost:8080` → Seldon service port `8000`.

**Run automated tests:**

```bash
# In another terminal (with port-forward running)
make k8s-ms-test
```

This runs multiple test cases (positive, negative, neutral, batch) against the model server.

**Manual test with curl:**

```bash
# Single prediction
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{"data":{"ndarray":[["This is amazing!"]]}}'

# Expected response:
# {"data":{"names":["t:0","t:1"],"ndarray":[["positive",0.95]]},"meta":{}}
```

**Batch predictions:**

```bash
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{"data":{"ndarray":[["Great product!"],["Not good"],["It works fine"]]}}'
```

## Step 5: Run the UI

The UI provides a web interface for sentiment analysis.

**In a new terminal:**

```bash
cd learn-seldon-core-v1
source .venv/bin/activate

# Ensure Seldon API is accessible
export SELDON_HOST=localhost
export SELDON_PORT=8080

# Start UI
make run-ui
```

**Access the UI:** Open http://localhost:8000 in your browser.

**Features:**
- Enter text to analyze sentiment
- Real-time predictions from Seldon Core
- Confidence scores displayed
- Beautiful, responsive interface

**Stop the UI:**

```bash
make stop-ui
```

## Step 6: View Logs and Monitor

**Stream model server logs:**

```bash
make k8s-ms-logs
```

**Check deployment status:**

```bash
make k8s-ms-status
```

**View Kubernetes resources:**

```bash
# All resources in seldon namespace
kubectl get all -n seldon

# Seldon deployments
kubectl get seldondeployments -n seldon

# Detailed pod info
kubectl describe pod -l seldon-deployment-id=sentiment-classifier -n seldon
```

## Common Commands

### Development

```bash
make data                      # Generate training data
make train                     # Train model
make notebook                  # Start Jupyter notebook
make clean-build-artifacts     # Clean Python caches
```

### Kubernetes

```bash
make k8s-deploy-model-server   # Deploy model to K8s
make k8s-ms-status             # Check status
make k8s-ms-logs               # Stream logs
make k8s-ms-port-fwd           # Port forward service to localhost:8080
make k8s-ms-test               # Run tests against model server
make k8s-clean                 # Delete all K8s resources
```

### Local UI

```bash
make run-ui                    # Start UI server
make stop-ui                   # Stop UI server
```

## Clean Up

When you're done:

```bash
# Delete Kubernetes resources
make k8s-clean

# Stop minikube
minikube stop

# Clean build artifacts
make clean-build-artifacts
```

## Next Steps

### Explore the Notebooks

```bash
make notebook
```

Check out:
- `notebooks/01_train_model.ipynb` - Training workflow
- `notebooks/02_inference_test.ipynb` - Interactive testing

### Customize the Model

1. **Modify training data:**
   - Edit `src/generate_data.py`
   - Run `make data` to regenerate

2. **Change model architecture:**
   - Edit `src/train_model.py`
   - Run `make train` to retrain

3. **Redeploy:**
   ```bash
   make k8s-clean
   make k8s-deploy-model-server
   ```

### Understand the Architecture

**Model Serving Architecture:**

```
User Browser
    ↓
FastAPI UI (localhost:8000)
    ↓
Seldon Core API (localhost:8080)
    ↓
SeldonDeployment (Kubernetes)
    ↓
Model Container (sentiment-seldon)
    ↓
SentimentClassifier Wrapper
    ↓
Scikit-learn Model
```

**Key Components:**

- **FastAPI UI** (`src/app.py`) - Web interface for users
- **Seldon Model** (`src/seldon_model.py`) - Seldon wrapper for the model
- **Trainer** (`src/train_model.py`) - Model training script
- **SeldonDeployment** (`k8s/seldon-deployment.yaml`) - Kubernetes CRD

### Deployment Options

**Local Development:**
- UI runs on your machine (port 8000)
- Model served by Seldon in minikube (port 8080)
- Good for development and testing

**Production Considerations:**
- Deploy UI to Kubernetes as well
- Use ingress controller instead of port forwarding
- Add authentication and rate limiting
- Use persistent volumes for models
- Implement monitoring and logging

## Troubleshooting

Having issues? See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for:

- [Setup problems](TROUBLESHOOTING.md#setup-issues)
- [Model server errors](TROUBLESHOOTING.md#seldon-core-issues)
- [Kubernetes issues](TROUBLESHOOTING.md#kubernetes-issues)
- [Port conflicts](TROUBLESHOOTING.md#port-conflicts)

**Quick fixes:**

- **Model not found:** `make train`
- **Minikube not running:** `minikube start`
- **UI can't connect:** Check port forwarding is active
- **Pods not starting:** `make k8s-ms-logs` to see errors

## Learning Resources

- [SETUP.md](SETUP.md) - Detailed setup guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [README.md](../README.md) - Project overview
- [Seldon Core Docs](https://docs.seldon.io/projects/seldon-core/en/v1.17.1/) - Official documentation

## API Reference

### Seldon Core v1 API

**Endpoint:** `http://localhost:8080/api/v1.0/predictions`

**Request format:**
```json
{
  "data": {
    "ndarray": [["text to analyze"]]
  }
}
```

**Response format:**
```json
{
  "data": {
    "names": ["t:0", "t:1"],
    "ndarray": [["positive", 0.95]]
  },
  "meta": {}
}
```

**Response fields:**
- `ndarray[0][0]` - Sentiment (positive/neutral/negative)
- `ndarray[0][1]` - Confidence score (0.0 to 1.0)

### FastAPI UI

**Endpoint:** `http://localhost:8000`

**Features:**
- Web form for text input
- Real-time sentiment analysis
- Displays sentiment and confidence
- Responsive design

---

**Need help?** Open an issue on GitHub or check [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
