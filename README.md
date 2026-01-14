# Sentiment Analyzer with Seldon Core v1

[![CI/CD Pipeline](https://github.com/r39132/learn-seldon-core-v1/actions/workflows/ci.yml/badge.svg)](https://github.com/r39132/learn-seldon-core-v1/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Seldon Core](https://img.shields.io/badge/Seldon%20Core-v1.17.1-green.svg)](https://github.com/SeldonIO/seldon-core)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A production-ready ML project demonstrating three-class sentiment analysis (Positive/Neutral/Negative) with model training, deployment, and serving using **Seldon Core v1** on Kubernetes.

> **⚠️ Educational Purpose**: The sentiment analysis model is intentionally simple (Logistic Regression with TF-IDF) to focus on Seldon Core v1 deployment patterns rather than state-of-the-art NLP.

## Overview

This project demonstrates:
- **Model Training**: Scikit-learn pipeline with TF-IDF vectorization
- **Model Serving**: Seldon Core v1 on Kubernetes with custom Python wrapper
- **Web Interface**: FastAPI UI for interactive sentiment analysis
- **Modern Tooling**: pyenv, direnv, uv for reproducible environments
- **Best Practices**: Type hints, testing, linting, pre-commit hooks

### Features

✅ **Three-class sentiment** (Positive/Neutral/Negative) with confidence scores
✅ **Seldon Core v1** production-grade model serving
✅ **FastAPI UI** for easy interaction
✅ **Complete automation** via Makefiles
✅ **Kubernetes deployment** on minikube
✅ **Jupyter notebooks** for interactive exploration

## Development, Testing, & Deployment

### Prerequisites

- **macOS** (or Linux/WSL2)
- **Homebrew** installed
- **4GB+ RAM** for Kubernetes
- **Docker Desktop** (for K8s deployment)

All development tools (Python, Java, pyenv, jenv, direnv, uv) are installed automatically.

### Setup

```bash
# Clone repository
gh repo clone <username>/learn-seldon-core-v1
cd learn-seldon-core-v1

# Run automated setup
make setup
```

This installs all tools, creates virtual environment, and installs dependencies.

**After setup:** Configure your shell and restart terminal (see [SETUP.md](docs/SETUP.md)).

### Quick Start

```bash
# Generate data and train model
make data
make train

# Deploy to Kubernetes
make k8s-deploy-model-server

# Start UI (in separate terminal)
kubectl port-forward svc/sentiment-classifier-default -n seldon 8080:8000
make run-ui
```

**Access UI:** http://localhost:8000

For detailed instructions, see [QUICKSTART.md](docs/QUICKSTART.md).

### Project Structure

```
learn-seldon-core-v1/
├── src/
│   ├── app.py                  # FastAPI UI application
│   ├── seldon_model.py         # Seldon Core v1 wrapper
│   ├── train_model.py          # Model training script
│   └── generate_data.py        # Training data generator
├── k8s/
│   └── seldon-deployment.yaml  # Seldon Core v1 CRD
├── notebooks/
│   ├── 01_train_model.ipynb    # Training workflow
│   └── 02_inference_test.ipynb # Testing predictions
├── models/                      # Trained model artifacts
├── data/                        # Training datasets
└── tests/                       # Unit tests
```

### Commands

**Development:**
```bash
make data                      # Generate training data
make train                     # Train model
make notebook                  # Start Jupyter notebook
make clean-build-artifacts     # Clean caches
```

**Kubernetes Deployment:**
```bash
make k8s-deploy-model-server   # Deploy model server
make k8s-ms-status             # Check deployment status
make k8s-ms-logs               # Stream logs
make k8s-clean                 # Delete all resources
```

**Local UI:**
```bash
make run-ui                    # Start UI server
make stop-ui                   # Stop UI server
```

**All commands:** Run `make help`

## Architecture

### Model Serving Flow

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
Scikit-learn Model (Logistic Regression + TF-IDF)
```

**Key Components:**

- **Seldon Core v1** - Model serving framework with CRD-based deployment
- **SeldonDeployment** - Kubernetes custom resource defining inference graph
- **Service Orchestrator** - Request routing and model execution
- **SentimentClassifier** - Python wrapper implementing Seldon API
- **FastAPI UI** - Web interface for user interaction

**Model Architecture:**
- Logistic Regression classifier
- TF-IDF vectorization (5000 features, 1-5 n-grams)
- Three sentiment classes: Positive, Neutral, Negative

## Documentation

| Document | Description |
|----------|-------------|
| **[QUICKSTART.md](docs/QUICKSTART.md)** | Get started in 5 minutes |
| **[SETUP.md](docs/SETUP.md)** | Detailed setup instructions |
| **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** | Common issues and solutions |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design and architecture |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Contribution guidelines |

## Troubleshooting

Having issues? See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

**Quick fixes:**
- [Tool installation problems](docs/TROUBLESHOOTING.md#tool-installation-issues)
- [Model server errors](docs/TROUBLESHOOTING.md#seldon-core-issues)
- [Kubernetes issues](docs/TROUBLESHOOTING.md#kubernetes-issues)
- [Port conflicts](docs/TROUBLESHOOTING.md#port-conflicts)
## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

This project is for educational purposes. See [CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md) for community guidelines.

---

**Built with:** Seldon Core v1.17.1 • FastAPI • Scikit-learn • Kubernetes • Python 3.12
