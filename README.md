# Sentiment Analyzer with Seldon Core v1

[![CI/CD Pipeline](https://github.com/r39132/learn-seldon-core-v1/actions/workflows/ci.yml/badge.svg)](https://github.com/r39132/learn-seldon-core-v1/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Seldon Core](https://img.shields.io/badge/Seldon%20Core-v1.17.1-green.svg)](https://github.com/SeldonIO/seldon-core)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](docs/CONTRIBUTING.md)

A production-ready ML project demonstrating three-class sentiment analysis (Positive/Neutral/Negative) with model training, deployment, and serving using **Seldon Core v1** on Kubernetes.

> **Note**: This project uses Seldon Core v1 (v1.17.1) which uses the `machinelearning.seldon.io/v1` API.

> **⚠️ Educational Purpose**: The sentiment analysis model is intentionally naive (Logistic Regression with TF-IDF) and designed for illustration purposes only. This project focuses on demonstrating Seldon Core v1 concepts and ML deployment patterns, not state-of-the-art NLP.

> **📸 [View Screenshots](screenshots/)** - See the UI in action

## 🎯 Features

- **Three-class sentiment** classification with confidence scores
- **Two deployment modes**:
  - **Seldon Core v1**: Production-grade model serving with SeldonDeployment CRD
  - **FastAPI**: Simplified standalone deployment for learning
- **Complete Seldon v1 integration**: Python wrapper, CRDs, and inference graphs
- **Modern Python tooling** (pyenv, jenv, direnv, uv)
- **Best practices** (linting, testing, type checking, pre-commit hooks)
- **Complete documentation** and Jupyter notebooks

## � Prerequisites

- **macOS** (or Linux/WSL2)
- **Homebrew** package manager
- **Git** for version control
- **4GB+ RAM** for Kubernetes deployment
- **Docker Desktop** (optional, for containerization)
- **minikube** (optional, for local K8s deployment)

> All other tools (Python, Java, pyenv, jenv, direnv, uv, gh) are installed automatically via `make setup`

## �📚 Documentation

| Guide | Description |
|-------|-------------|
| [TOOLS_SETUP.md](docs/TOOLS_SETUP.md) | Install pyenv, jenv, direnv, uv, gh |
| [GETTING_STARTED.md](docs/GETTING_STARTED.md) | Step-by-step tutorial |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Kubernetes deployment (FastAPI version) |
| [SELDON_DEPLOYMENT.md](docs/SELDON_DEPLOYMENT.md) | **Seldon Core v1 deployment guide** |
| [QUICKREF.md](docs/QUICKREF.md) | Quick command reference |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture |
| [blog.md](docs/blog.md) | Deep dive into Seldon Core v1 |

## 🏗️ Architecture

**Two Deployment Options:**

### Option 1: Seldon Core v1 (Production)
```
REST API → Seldon Service Orchestrator → Model Container → SentimentClassifier
```

**Components:**
- **Seldon Operator** - Manages SeldonDeployment lifecycle
- **Service Orchestrator** - Request routing and graph execution
- **Model Container** - Custom Python wrapper with scikit-learn model
- **Scikit-Learn** - Logistic Regression + TF-IDF (3 classes, 5000 features, 1-5 n-grams)

### Option 2: FastAPI (Learning/Development)
```
User Browser → FastAPI UI (8000) → Model Server (8001) → Scikit-Learn Model
```

**Components:**
- **FastAPI UI** - Web interface for text input
- **Model Server** - Simple FastAPI endpoint
- **Scikit-Learn** - Same model as Seldon deployment

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design.

> **📖** See [GETTING_STARTED.md](docs/GETTING_STARTED.md) for step-by-step tutorial and [TOOLS_SETUP.md](docs/TOOLS_SETUP.md) for tool installation.

## 🛠️ Available Commands

```bash
make help                # Show all commands
make setup               # Initial setup
make install             # Install dependencies
make data                # Generate training data
make train               # Train model
make test                # Run tests
make test-cov            # Tests with coverage
make lint                # Run linters
make format              # Format code
make run                 # Start FastAPI UI + model server (non-Seldon)
make stop                # Stop all servers
make restart             # Restart servers
make notebook            # Start Jupyter notebook
make docker-build        # Build all Docker images
make docker-build-seldon # Build only Seldon model image
make k8s-deploy          # Deploy FastAPI version to K8s
make k8s-deploy-model-server   # Deploy model server with Seldon Core v1
make clean-k8s           # Cleanup K8s resources
make clean-build-artifacts   # Clean generated files
```

## 📁 Project Structure

```
learn-seldon-core-v1/
├── src/              # Source code
│   ├── app.py              # FastAPI UI application
│   ├── model_server.py     # FastAPI model server (non-Seldon)
│   ├── seldon_model.py     # Seldon Core v1 Python wrapper
│   ├── train_model.py      # Model training script
│   └── generate_data.py    # Data generation
├── tests/            # Unit tests with pytest
├── notebooks/        # Jupyter notebooks for exploration
├── k8s/              # Kubernetes manifests
│   ├── namespace.yaml               # Namespace definition
│   ├── seldon-deployment.yaml       # SeldonDeployment CRD (Seldon Core v1)
│   ├── model-server-deployment.yaml # FastAPI deployment (non-Seldon)
│   └── fastapi-deployment.yaml      # FastAPI UI deployment
├── scripts/          # Utility scripts
│   ├── deploy-seldon.sh   # Deploy with Seldon Core
│   ├── deploy-k8s.sh      # Deploy FastAPI version
│   ├── test-seldon.sh     # Test Seldon deployment
│   └── setup.sh           # Initial setup
├── .s2i/             # Seldon s2i configuration
├── data/             # Training data (raw/processed)
├── models/           # Trained models (.pkl files)
├── Dockerfile.seldon      # Seldon model container
├── Dockerfile.modelserver # FastAPI model server
├── Dockerfile.fastapi     # FastAPI UI
└── Makefile          # Task automation - run `make help`
```

## 🧪 Development

All development tasks are automated via Makefile:

```bash
make test          # Run tests
make test-cov      # Tests + coverage report
make lint          # Check code quality
make format        # Auto-format code
make notebook      # Start Jupyter
make validate      # Verify project setup
```

Pre-commit hooks run automatically on `git commit` to ensure code quality.

## 🐳 Docker & Kubernetes

```bash
make docker-build  # Build both images
make k8s-deploy    # Deploy to Kubernetes
make clean-k8s     # Cleanup resources
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed Kubernetes operations, troubleshooting, and advanced configurations.

## 📚 Notebooks

- `notebooks/01_train_model.ipynb` - Model training workflow
- `notebooks/02_inference_test.ipynb` - Inference testing

Run with `make notebook` or `make jupyter`

## 🔍 Troubleshooting

For common issues and solutions, see [DEPLOYMENT.md](docs/DEPLOYMENT.md) and [QUICKREF.md](docs/QUICKREF.md).

**Quick fixes:**
- Model not found? Run `make train`
- Environment issues? Run `make validate`
- Port conflicts? Check with `lsof -i :8000`

## 🤝 Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📄 License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

This project is for educational purposes. See [CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md) for community guidelines.

---

**Built with:** Seldon Core • FastAPI • Scikit-learn • Kubernetes
