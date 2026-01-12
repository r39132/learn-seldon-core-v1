# Sentiment Analyzer with Seldon Core

A production-ready ML project demonstrating three-class sentiment analysis (Positive/Neutral/Negative) with model training, deployment, and serving using Seldon Core on Kubernetes.

## 🎯 Features

- **Three-class sentiment** classification with confidence scores
- **Seldon Core** model serving on Kubernetes
- **FastAPI** web UI with beautiful interface
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
| [TOOLS_SETUP.md](TOOLS_SETUP.md) | Install pyenv, jenv, direnv, uv, gh |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Step-by-step tutorial |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Kubernetes deployment |
| [QUICKREF.md](QUICKREF.md) | Quick command reference |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |

## 🏗️ Architecture

```
User Browser → FastAPI UI (8000) → Seldon Core (9000) → Scikit-Learn Model
```

**Components:**
- **FastAPI UI** - Web interface for text input
- **Seldon Core** - Model serving platform
- **Scikit-Learn** - Logistic Regression + TF-IDF (3 classes, 5000 features)

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design.

> **📖** See [GETTING_STARTED.md](GETTING_STARTED.md) for step-by-step tutorial and [TOOLS_SETUP.md](TOOLS_SETUP.md) for tool installation.

## 🛠️ Available Commands

```bash
make help          # Show all commands
make setup         # Initial setup
make install       # Install dependencies
make data          # Generate training data
make train         # Train model
make test          # Run tests
make test-cov      # Tests with coverage
make lint          # Run linters
make format        # Format code
make run-local     # Run UI + model server (recommended for local dev)
make run           # Run FastAPI UI only (needs model server)
make run-model-server  # Run model server only
make notebook      # Start Jupyter notebook
make docker-build  # Build Docker images
make k8s-deploy    # Deploy to Kubernetes
make k8s-clean     # Cleanup K8s resources
make validate      # Validate project
make clean         # Clean generated files
```

## 📁 Project Structure

```
learn-seldon/
├── src/           # Source code (app.py, train_model.py, generate_data.py, etc.)
├── tests/         # Unit tests with pytest
├── notebooks/     # Jupyter notebooks for exploration
├── k8s/           # Kubernetes manifests
├── scripts/       # Utility scripts (setup.sh, deploy-k8s.sh)
├── data/          # Training data (raw/processed)
├── models/        # Trained models (.pkl files)
└── Makefile       # Task automation - run `make help`
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
make k8s-clean     # Cleanup resources
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Kubernetes operations, troubleshooting, and advanced configurations.

## 📚 Notebooks

- `notebooks/01_train_model.ipynb` - Model training workflow
- `notebooks/02_inference_test.ipynb` - Inference testing

Run with `make notebook` or `make jupyter`

## 🔍 Troubleshooting

For common issues and solutions, see [DEPLOYMENT.md](DEPLOYMENT.md) and [QUICKREF.md](QUICKREF.md).

**Quick fixes:**
- Model not found? Run `make train`
- Environment issues? Run `make validate`
- Port conflicts? Check with `lsof -i :8000`

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

Educational purposes. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community guidelines.

---

**Built with:** Seldon Core • FastAPI • Scikit-learn • Kubernetes
